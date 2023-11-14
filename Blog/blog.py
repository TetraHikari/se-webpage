from fastapi import APIRouter, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .models import*
from .blog_services import*

blog_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@blog_router.get("/se-blog", response_class=HTMLResponse)
async def se_blog(request: Request, username: str = Cookie(None), email: str = Cookie(None), year: int = Cookie(None)):
    # Retrieve all posts from the database
    print(get_all_post())
    
# @blog_router.post("/create-post")
# async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
#     username = request.cookies.get("username")
#     user = root.get(username)
#     if user:
#         user.create_post(title, content)
#         connection.transaction_manager.commit()
#         return {"message": "Post created successfully"}
#     else:
#         return {"message": "User not found"}


# @blog_router.post("/delete-post/{post_id}")
# async def delete_post(request: Request, post_id: str):
#     username = request.cookies.get("username")
#     user = root.get(username)
#     if user:
#         user.delete_post(post_id)
#         connection.transaction_manager.commit()
#         return {"message": "Post deleted successfully"}
#     else:
#         return {"message": "User not found"}



