from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.staticfiles import StaticFiles

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Depends

import bcrypt

import json

app = FastAPI()

# Database configuration
MONGODB_URL = "mongodb+srv://peeranatpee1:Peeranat1205HB@cluster0.ybeo3du.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "myDatabase"
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def verify_password(username: str, password: str):
    print(f"Verifying password for user: {username}")
    user = await db.users.find_one({"username": username})
    print(f"User data from MongoDB: {user}")
    if not user:
        print("User not found")
        return False
    is_valid = bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8'))
    print(f"Password is valid: {is_valid}")
    return is_valid


@app.get("/")
def read_root(request: Request):
    # This is an example of passing dynamic content to the template.
    context = {"request": request, "name": "User"}
    return templates.TemplateResponse("index.html", context)

@app.get("/userlogin")
def userlogin_page(request: Request):
    return templates.TemplateResponse("user-login.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not await verify_password(username, password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"success": True}


@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    user = await db.users.find_one({"username": username})
    if user:
        return {"error": "Username already exists"}
    hashed_password = hash_password(password)
    await db.users.insert_one({"username": username, "password": hashed_password})
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)