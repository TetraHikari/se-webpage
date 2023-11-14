from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.templating import Jinja2Templates
from Login.login import login_router
from Blog.blog import blog_router

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

app.include_router(login_router)

app.include_router(blog_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)