from fastapi import APIRouter, Request, Form, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ZODB import FileStorage, DB
from models import*
import sys
import os


current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*


login_router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Retrieve data from the database
storage = FileStorage.FileStorage('db/account.fs')
db = DB(storage)
connection = db.open()


# for account in root:
#     print(root[account].username)
#     print(root[account].email)
#     print(root[account].password)
    



@login_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@login_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)
    root = connection.root()
    for account in root:
        if root[account].username == user.username and root[account].password == user.password:
            return templates.TemplateResponse("main-menu.html", {"request": request})
        else:
            return {"message": "Invalid username or password"}
    
    db.close()
    connection.close()

    
    

    