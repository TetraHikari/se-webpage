from fastapi import FastAPI, Request, Form, Cookie, Response,requests, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sys
from Login.models import*
import datetime
from Blog.models import*
from Blog.BlogServ import*
import sys,os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
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
    return RedirectResponse(url="/login", status_code=302)

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
            print("Account:", account)            
            # Print specific attributes
            print("Username:", current_account.username)
            print("Email:", current_account.email)
            print("Password:", current_account.password)
            print("Year:", current_account.year)
            print("Fullname:", current_account.get_fullname())
            
            if current_account.username == user.username and current_account.password == user.password:
                response = RedirectResponse("/main-menu", status_code=302)
                response.set_cookie(key="username", value=current_account.username)
                response.set_cookie(key="email", value=current_account.email)
                response.set_cookie(key="firstname", value=current_account.name)
                response.set_cookie(key="lastname", value=current_account.lastname)
                response.set_cookie(key="year", value=current_account.year)
                response.set_cookie(key="fullname", value=current_account.get_fullname())
                shutdown_db_client()
                return response
            
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    finally:
        shutdown_db_client()

@app.get("/main-menu", response_class=HTMLResponse)
async def main_menu(request: Request, username: str = Cookie(None), fullname: str = Cookie(None), email: str = Cookie(None), year: int = Cookie(None)):
    return templates.TemplateResponse("main-menu.html", {"request": request,"username": username, "fullname": fullname, "email": email, "year": year})

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
        post_id = str(uuid.uuid4())

        # Create a new post
        post = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": datetime.datetime.now().ctime()
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
    print(all_posts)

    # Return the updated blog page
    return templates.TemplateResponse("blog.html", {"request": request, "username": username, "posts": all_posts})



@app.post("/delete-post/{post_id}", response_class=HTMLResponse)
async def delete_post(request: Request, post_id: str, username: str = Cookie(None)):
    root = open_db_client()
    updated_posts = []

    try:
        for user in root:
            # Create a copy of the keys to avoid RuntimeError
            user_posts_keys = list(root[user].posts.keys())
            
            for post_key in user_posts_keys:
                if post_key == post_id:
                    print(f"Username: {user}, Post ID: {post_id}")
                    del root[user].posts[post_key]
        commit()

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)