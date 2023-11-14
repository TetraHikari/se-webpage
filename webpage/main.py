from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import*
import uvicorn

account = {
    "65011610" : "123456",
    "65011611" : "123456",
    "65011612" : "123456",
}

app = FastAPI()
templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request:Request,username: str = Form(...), password: str = Form(...)):
    if username in account and account[username] == password:
        return templates.TemplateResponse("main-menu.html", {"request": request, "username": username})
    else:
        return {"status": "failure"}
    

@app.get("/menu")
async def main_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})
    
@app.get("/dashboard")
async def main_menu(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})    

@app.get("/se-blog")
async def se_blog(request: Request):
    # Retrieve all posts from the MongoDB collection
    posts = collection.find({})
    
    # Pass the retrieved posts to the HTML template
    return templates.TemplateResponse("blog.html", {"request": request, "posts": posts})



@app.post("/delete-post/{post_id}")
async def delete_post(request: Request, post_id: str):
    # Delete the post from the MongoDB collection
    collection.delete_one({"_id": ObjectId(post_id)})

    # Redirect back to the homepage
    return RedirectResponse(url="/se-blog", status_code=303)


@app.post("/create-post")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
    post = Post(title=title, content=content, created_at=datetime.now().ctime())
    collection.insert_one(post.dict())
        # Retrieve all posts from the MongoDB collection
    posts = collection.find({})
    
    return RedirectResponse(url="/se-blog", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)