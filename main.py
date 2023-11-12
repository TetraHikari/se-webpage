from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
async def login(username: str = Form(...), password: str = Form(...)):
    if username in account and account[username] == password:
        return {"status": "success"}
    else:
        return {"status": "failure"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)