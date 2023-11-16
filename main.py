from fastapi import FastAPI, Request, Form, Cookie, Response,requests, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sys, os
from Login.models import*
import datetime
from Blog.models import*
from Blog.BlogServ import*
from Library.models import*
from Library.LibraryServ import*
from RoomReser.models import*
from RoomReser.RoomServ import*
from db.database import*
app = FastAPI()
templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

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
    #initializing database
    # root = open_db_client()

    # # Create 5 example accounts
    # create_account(root, "65011610", "65011610@kmitl", "123456", 1, "Peeranat", "Patarakittisopol")
    # create_account(root, "65011611", "65011611@kmitl", "123456", 2, "Peeranat", "Patarakittisopol")
    # create_account(root, "65011612", "65011612@kmitl", "123456", 3, "Peeranat", "Patarakittisopol")
    # create_account(root, "65011613", "65011613@kmitl", "123456", 4, "Peeranat", "Patarakittisopol")

    # # Create 5 example books
    # create_book(root, "The Hunger Games", "Suzanne Collins", 2008, "Science Fiction", "978-0439023481", "https://www.amazon.com/Hunger-Games-Book/dp/B002MQYOFW")    
    # create_book(root, "Harry Potter and the Philosopher's Stone", "J. K. Rowling", 1997, "Fantasy", "978-0747532743", "https://www.amazon.com/Harry-Potter-Philosophers-Stone-Rowling/dp/0747532745")
    # create_book(root, "To Kill a Mockingbird", "Harper Lee", 1960, "Fiction", "978-0446310789", "https://www.amazon.com/Kill-Mockingbird-Harper-Lee/dp/0446310786")
    # create_book(root, "Pride and Prejudice", "Jane Austen", 1813, "Romance", "978-0141439518", "https://www.amazon.com/Pride-Prejudice-Jane-Austen/dp/0141439513")
    # create_book(root, "Twilight", "Stephenie Meyer", 2005, "Fantasy", "978-0316015844", "https://www.amazon.com/Twilight-Saga-Book-1/dp/0316015849")

    # create_room(root, "Room101", "Small meeting room", 10)
    # create_room(root, "Room102", "Medium meeting room", 15)
    # create_room(root, "Room201", "Large meeting room", 20)
    # create_room(root, "Room202", "Conference room", 30)
    # create_room(root, "Room301", "Training room", 25)

    # shutdown_db_client()

    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)
    root = open_db_client()
    try:
        for account in root:
            current_account = root[account]
            print("Account:", account)            
            # Print specific attributes
            print("Username:", current_account.username)
            print("Email:", current_account.email)
            print("Password:", current_account.password)
            print("Year:", current_account.year)
            print("Fullname:", current_account.get_fullname())
            
            if current_account.username == user.username and current_account.password == user.password:
                response = templates.TemplateResponse("main-menu.html", {"request": request, "username": current_account.username, "email": current_account.email, "year": current_account.year, "name": current_account.get_fullname()})
                response.set_cookie(key="username", value=current_account.username)
                response.set_cookie(key="email", value=current_account.email)
                response.set_cookie(key="firstname", value=current_account.name)
                response.set_cookie(key="lastname", value=current_account.lastname)
                response.set_cookie(key="year", value=current_account.year)
                shutdown_db_client()
                return response
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        shutdown_db_client()

@app.get("/main-menu", response_class=HTMLResponse)
async def main_menu(request: Request, username: str = Cookie(None), email: str = Cookie(None), year: int = Cookie(None)):
    return templates.TemplateResponse("main-menu.html", {"request": request, "username": username, "email": email, "year": year})

#Blog

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
        user_year = root[username].year


        post_id = str(uuid.uuid4())

        # Create a new post
        post = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": datetime.datetime.now().ctime(),
            "like":0,
            "postedby": f"{username} (Year: {user_year})",  # Combine username and year
            "yearpost": f"{user_year}",
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

@app.get("/room-reservation", response_class=HTMLResponse)
async def room_reservation(request: Request, username: str = Cookie(None)):
    root = open_db_client()
    try:
        rooms = []
        
        for room_id in root.keys():
            if isinstance(root[room_id], Room):
                rooms.append(room_detail(root, room_id))
        print(rooms)

        return templates.TemplateResponse("room.html", {"request": request, "rooms": rooms})
    finally:
        shutdown_db_client()

@app.post("/reserve-room", response_class=HTMLResponse)
async def reserve_room(request: Request, room_id: str = Form(...), username: str = Cookie(None)):
    root = open_db_client()
    try:
        reserved_room(root, room_id)
        rooms = []
        for room_id in root.keys():
            if isinstance(root[room_id], Room):
                rooms.append(room_detail(root, room_id))
        print(rooms)
        return templates.TemplateResponse("room.html", {"request": request, "rooms": rooms})
    finally:
        shutdown_db_client()

@app.get("/library", response_class=HTMLResponse)
async def library(request: Request, username: str = Cookie(None)):
    root = open_db_client()
    try:
        books = []
        
        for book_id in root.keys():
            if isinstance(root[book_id], Book):
                books.append(book_detail(root, book_id))
        print(books)

        return templates.TemplateResponse("library.html", {"request": request, "books": books})
    finally:
        shutdown_db_client()

@app.post("/add-book", response_class=RedirectResponse)
async def add_book(request: Request, title: str = Form(...), author: str = Form(...), year: int = Form(...), genre: str = Form(...), isbn: str = Form(...), url: str = Form(...), username: str = Cookie(None)):
    root = open_db_client()
    try:
        create_book(root, title, author, year, genre, isbn, url)
        books = []
        for book_id in root.keys():
            if isinstance(root[book_id], Book):
                books.append(book_detail(root, book_id))
        print(books)
        return RedirectResponse(url=f"/library", status_code=303)
    finally:
        shutdown_db_client()

# @app.post("/delete-post/{post_id}", response_class=HTMLResponse)
# async def delete_post(request: Request, post_id: str, username: str = Cookie(None)):
#     root = open_db_client()
#     updated_posts = []

#     try:
#         # Check if the post belongs to the current user
#         if username not in root or post_id not in root[username].posts:
#             raise HTTPException(status_code=403, detail="Permission denied: Post not found or does not belong to the user")

#         # Delete the post
#         del root[username].posts[post_id]
#         commit()

#         # Update the posts for the current user
#         for user in root:
#             account_posts = read_all_post(root, user)
#             updated_posts.extend(account_posts)

#     except HTTPException as e:
#         raise e
#     finally:
#         # Close the database connection
#         shutdown_db_client()

#     # Return the updated blog page
#     return templates.TemplateResponse("blog.html", {"request": request, "username": username, "posts": updated_posts})

@app.post("/delete-post/{post_id}", response_class=RedirectResponse)
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
    return RedirectResponse(url=f"/se-blog", status_code=303)




# Update the like_post function in main.py
# @app.post("/like-post/{post_id}/{current_username}", response_class=HTMLResponse)
# async def like_post(request: Request, post_id: str, current_username: str):
#     root = open_db_client()
#     updated_posts = []

#     try:
#         for user in root:
#             for post in read_all_post(root, user):
#                 if post["post_id"] == post_id:
#                     # Check if the user has already liked the post
#                     if current_username not in post["liked_by"]:
#                         add_like(root, post_id, post["like"] + 1, current_username)

#         # Update the posts for the current user
#         for user in root:
#             account_posts = read_all_post(root, user)
#             updated_posts.extend(account_posts)

#     except HTTPException as e:
#         raise e
#     finally:
#         # Close the database connection
#         shutdown_db_client()

#     # Return the updated blog page with the like count
#     return templates.TemplateResponse("blog.html", {"request": request, "posts": updated_posts, "username": current_username})

@app.post("/like-post/{post_id}/{current_username}", response_class=RedirectResponse)
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
    return RedirectResponse(url=f"/se-blog", status_code=303)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)