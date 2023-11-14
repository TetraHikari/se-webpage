from fastapi import APIRouter, Request, Form, Cookie, Response
from fastapi.responses import*
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

@login_router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@login_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)
    root = open_db_client()
    
    for account in root:
        if root[account].username == user.username and root[account].password == user.password:
            
            response = templates.TemplateResponse("main-menu.html", {"request": request})
            response.set_cookie(key="username", value=root[account].username)
            response.set_cookie(key="email", value=root[account].email)
            response.set_cookie(key="year", value=root[account].year)

            return response
        else:
            return {"message": "Invalid username or password"}
    
    shutdown_db_client()
    


        
        
        




    
    

    