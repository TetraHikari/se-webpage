from fastapi import FastAPI, Request, Form, Cookie, Response,requests, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import sys
from Login.models import*
import datetime
from Blog.models import*
from Blog.BlogServ import*
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
        post_id = str(uuid.uuid4())

        # Create a new post
        post = Post(post_id=post_id,title=title, content=content, created_at=datetime.datetime.now().ctime())

        # Add the post to the user's posts in the database
        root[username].posts[post_id] = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": datetime.datetime.now().ctime()
        }

        # Commit the changes to the database
        commit()
        
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
    print(f"Username: {username}, Post ID: {post_id}")
    print(read_all_post(root, username))

    try:
        # Ensure the user exists in the database
        if username not in root:
            raise HTTPException(status_code=404, detail="User not found")

        # Ensure the post exists in the user's posts
        if post_id not in root[username].posts:
            raise HTTPException(status_code=404, detail="Post not found")

        # Delete the post from the user's posts in the database
        del root[username].posts[post_id]

        # Commit the changes to the database
        commit()
    except HTTPException as e:
        raise e
    finally:
        # Close the database connection
        shutdown_db_client()

    # Return the updated blog page
    return templates.TemplateResponse("blog.html", {"request": request, "username": username, "posts": read_all_post(root, username)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)