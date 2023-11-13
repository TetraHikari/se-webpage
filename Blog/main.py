from fastapi import APIRouter, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models import*
import uvicorn

blog_router = APIRouter()
templates = Jinja2Templates(directory="../templates")

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
    
    # Redirect back to the blog page
    posts = collection.find({})
    return templates.TemplateResponse("blog.html", {"request": request, "posts": posts})

@app.post("/create-post")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
    post = Post(title=title, content=content, created_at=datetime.now().ctime())
    collection.insert_one(post.dict())
        # Retrieve all posts from the MongoDB collection
    posts = collection.find({})
    
    return templates.TemplateResponse("blog.html", {"request": request, "posts": posts})

