from fastapi import FastAPI, Request, Form, Cookie, Response,requests, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
import sys
from Login.models import*
import datetime
from Blog.models import*
from Blog.BlogServ import*
from Grade.GradeServ import*
from Grade.models import*
from RoomReser.RoomServ import*
sys.path.insert(1, 'C:\\Users\\Acer\\Desktop\\SE_Website\\db')
from db.database import*


app = FastAPI()
templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

from fastapi.responses import RedirectResponse

@app.post("/logout", response_class=RedirectResponse)
async def logout(response: Response, request: Request):
    # Clear the cookies to log out the user
    response.delete_cookie("username")
    response.delete_cookie("email")
    response.delete_cookie("year")
    
    # Redirect to the home page or login page
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)
    root = open_db_client()

    try:
        for account in root:
            current_account = root[account]

            if isinstance(current_account, Student):
                # Check if the account is a student
                if current_account.username == user.username and current_account.password == user.password:
                    response = templates.TemplateResponse("main-menu.html", {
                        "request": request,
                        "username": current_account.username,
                        "email": current_account.email,
                        "year": current_account.year,
                        "name": current_account.get_fullname(),
                        "subjects": get_subject_from_student(root, current_account.username)
                    })
                    response.set_cookie(key="username", value=current_account.username)
                    response.set_cookie(key="email", value=current_account.email)
                    response.set_cookie(key="firstname", value=current_account.firstname)
                    response.set_cookie(key="lastname", value=current_account.lastname)
                    response.set_cookie(key="year", value=current_account.year)
                    return response

            elif isinstance(current_account, Professor):
                # Check if the account is a professor
                if current_account.username == user.username and current_account.password == user.password:
                    subject = get_subject_from_professor(root, current_account.username)
                    response = templates.TemplateResponse("main-menu.html", {
                        "request": request,
                        "username": current_account.username,
                        "email": current_account.email,
                        "subjects": subject,
                        "name": current_account.firstname + " " + current_account.lastname,
                        "is_professor": True
                    })
                    response.set_cookie(key="username", value=current_account.username)
                    response.set_cookie(key="email", value=current_account.email)
                    response.set_cookie(key="firstname", value=current_account.firstname)
                    response.set_cookie(key="lastname", value=current_account.lastname)
                    #save subject to cookie as List
                    response.set_cookie(key="subject", value=subject)
                    return response

    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        shutdown_db_client()


@app.get("/main-menu", response_class=HTMLResponse)
async def main_menu(request: Request, username: str = Cookie(None), email: str = Cookie(None), year: int = Cookie(None), firstname: str = Cookie(None), lastname: str = Cookie(None), subject: str = Cookie(None)):
    return templates.TemplateResponse("main-menu.html", {"request": request, "username": username, "email": email, "year": year, "name": firstname+" "+lastname, "subject": subject})



@app.get("/se-blog", response_class=HTMLResponse)
async def se_blog(request: Request, username: str = Cookie(None), email: str = Cookie(None), year: int = Cookie(None)):
    root = open_db_client()
    all_posts = []

    try:
        # Iterate over all accounts in the database
        for user in root:
            account_posts = read_all_post(root, user)
            all_posts.extend(account_posts)
    finally:
        shutdown_db_client()

    return templates.TemplateResponse("blog.html", {"request": request, "username": username, "email": email, "year": year, "posts": all_posts})

@app.post("/create-post", response_class=HTMLResponse)
async def create_post(request: Request, title: str = Form(...), content: str = Form(...), username: str = Cookie(None)):
    root = open_db_client()
    all_posts = []

    try:
        # Ensure the user exists in the database
        if username not in root:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate a unique post_id using UUID
        post_id = str(uuid.uuid4())

        # Create a new post
        post = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": datetime.datetime.now().ctime(),
            "like":0
        }

        # Add the post to the user's posts in the database
        root[username].posts[post_id] = post

        # Commit the changes to the database
        commit()

        # Iterate over all accounts in the database and collect posts
        for user in root:
            account_posts = read_all_post(root, user)
            all_posts.extend(account_posts)

    except HTTPException as e:
        raise e
    finally:
        # Close the database connection
        shutdown_db_client()

    # Return the updated blog page
    return templates.TemplateResponse("blog.html", {"request": request, "username": username, "posts": all_posts})

@app.post("/delete-post/{post_id}", response_class=HTMLResponse)
async def delete_post(request: Request, post_id: str, username: str = Cookie(None)):
    root = open_db_client()
    updated_posts = []

    try:
        # Check if the post belongs to the current user
        if username not in root or post_id not in root[username].posts:
            raise HTTPException(status_code=403, detail="Permission denied: Post not found or does not belong to the user")

        # Delete the post
        del root[username].posts[post_id]
        commit()

        # Update the posts for the current user
        for user in root:
            account_posts = read_all_post(root, user)
            updated_posts.extend(account_posts)

    except HTTPException as e:
        raise e
    finally:
        # Close the database connection
        shutdown_db_client()

    # Return the updated blog page
    return templates.TemplateResponse("blog.html", {"request": request, "username": username, "posts": updated_posts})

@app.post("/like-post/{post_id}/{current_username}", response_class=HTMLResponse)
async def like_post(request: Request, post_id: str, current_username: str):
    root = open_db_client()
    updated_posts = []

    try:
        for user in root:
            for post in read_all_post(root, user):
                if post["post_id"] == post_id:
                    # Check if the user has already liked the post
                    if current_username not in post["liked_by"]:
                        add_like(root, post_id, post["like"] + 1, current_username)

        # Update the posts for the current user
        for user in root:
            account_posts = read_all_post(root, user)
            updated_posts.extend(account_posts)

    except HTTPException as e:
        raise e
    finally:
        # Close the database connection
        shutdown_db_client()

    # Return the updated blog page with the like count
    return templates.TemplateResponse("blog.html", {"request": request, "posts": updated_posts, "username": current_username})



@app.get("/assign-grade", response_class=HTMLResponse)
async def assign_grade(request: Request, username: str = Cookie(None), subject: str = Cookie(None)):
    # Open the database connection
    root = open_db_client()

    try:
        students = get_student_from_subject(root, subject[2:-2])
        return templates.TemplateResponse("assign-grade.html",
                                          {"request": request, 
                                           "username": username,
                                           "subject": subject[2:-2],
                                           "students": students})
    finally:
        # Close the database connection
        shutdown_db_client()

@app.get("/grades", response_class=HTMLResponse)
async def grades(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse("grades.html", {"request": request, "username": username})

@app.post("/assign-grade", response_class=HTMLResponse)
async def grades(request: Request, username: str = Cookie(None)):
    return templates.TemplateResponse("grades.html", {"request": request, "username": username})

@app.post("/submit-grades", response_class=HTMLResponse)
async def submit_grades(
    request: Request,
    username: str = Cookie(None),
    subject: str = Cookie(None),
    scores: List[int] = Form(...),
    student_usernames: List[str] = Form(...),
):
    root = open_db_client()
    try:
        # Assuming scores and student_usernames are in the same order
        student_grade_info = list(zip(student_usernames, scores))

        # Process the grades and update your database
        for student_username, score in student_grade_info:
            # Update the database with the score for each student
            print(f"Student {student_username} got a score of {score} in {subject[2:-2]}")
            student_set_score(root, student_username, subject[2:-2], score)
            
        
        return templates.TemplateResponse("main-menu.html", {"request": request, "subject": subject})
    finally:
        shutdown_db_client()
        
@app.get("/view-grades", response_class=HTMLResponse)
async def view_grade(request: Request, username: str = Cookie(None), subject: str = Cookie(None)):
    root = open_db_client()
    try:
        subjects = []
        scores = []
        for subject_name, score in read_student_score(root, username).items():
            subjects.append(subject_name)
            scores.append(score)
        reservation_details = reservation_detail(root, username)
            
        return templates.TemplateResponse("view-grades.html",
                                              {"request": request,
                                               "username": username,
                                               "name": root[username].get_fullname(),
                                               "subject": subjects,
                                               "scores": read_student_score(root, username),
                                               "reservation_details": reservation_details,}
                                            )
    finally:
        # Close the database connection
        shutdown_db_client()
        
        
@app.get("/room-reservation", response_class=HTMLResponse)
async def read_item(
    request: Request,
    username: str = Cookie(None),
):
    root = open_db_client()
    try:
        times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        
        rooms = []
        for time in times:
            rooms.append(get_room_from_timeslot(root, time))
        reservation_details = reservation_detail(root, username)
        
        return templates.TemplateResponse(
            "room.html",
            {
                "request": request,
                "times": times,
                "rooms": rooms,
                "username": username,
                "reservation_details": reservation_details,
            },
        )
    finally:
        shutdown_db_client()
        
        from fastapi import Form, HTTPException

from fastapi.responses import HTMLResponse

@app.post("/submit-reservation", response_class=HTMLResponse)
async def submit_reservation(
    request: Request,
    username: str = Cookie(None),
    room: str = Form(...),
    begin_time: str = Form(...),
    end_time: str = Form(...),
):
    times = ["08:00", "09:00", "10:00", "11:00", "12:00",
             "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
             
    begin_time_index = times.index(begin_time)
    end_time_index = times.index(end_time)
    
    root = open_db_client()
    try:
        if end_time_index <= begin_time_index:
            raise HTTPException(status_code=400, detail="Invalid time range")
        
        if username not in root:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the room is already reserved during the selected time slot
        for i in range(begin_time_index, end_time_index):
            if root[room].reservation[times[i]]["status"] == "reserved":
                raise HTTPException(status_code=400, detail="Room is already reserved")
        
        # Reserve the room for the selected time slot
        for i in range(begin_time_index, end_time_index+1):
            reserve_room(root, room, times[i], username)
                
        # Get the updated list of reserved rooms
        updated_rooms = []
        for time in times:
            updated_rooms.append(get_room_from_timeslot(root, time))
        reservation_details = reservation_detail(root, username)
        
        # Display the updated rooms in the response
        return templates.TemplateResponse(
            "room.html",
            {
                "request": request,
                "times": times,
                "rooms": updated_rooms,
                "username": username,
                "reservation_details": reservation_details,
            },
        )
    finally:
        shutdown_db_client()
        
@app.post("/cancel-reservation", response_class=HTMLResponse)
async def cancel_reservation(
    request: Request,
    username: str = Cookie(None),
    room_id: str = Form(...),
    begin_time: str = Form(...),
    end_time: str = Form(...),
):
    root = open_db_client()
    try:
        times = ["08:00", "09:00", "10:00", "11:00", "12:00",
                 "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        begin_time_index = times.index(begin_time)
        end_time_index = times.index(end_time)
        # Check if the user has a reservation for the specified time slot
        for time_slot in times[begin_time_index:end_time_index+1]:
            if root[room_id].reservation[time_slot]["status"] == "reserved" and \
               root[room_id].reservation[time_slot]["username"] == username:
                # Cancel the reservation
                cancel_room_reservation(root, room_id, time_slot)
                commit()

                # Redirect to the room reservation page with updated details
                return templates.TemplateResponse(
                    "room.html",
                    {
                        "request": request,
                        "times": ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
                        "rooms": get_room_from_timeslot(root, time_slot),
                        "username": username,
                        "reservation_details": reservation_detail(root, username),
                    },
                )

        # If no reservation found for the specified time slot
        raise HTTPException(status_code=404, detail="Reservation not found for the specified time slot")

    finally:
        shutdown_db_client()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)