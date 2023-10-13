from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def verify_password(username: str, password: str):
    users = get_users()
    user = users.get(username)
    if not user:
        return False
    return user["password"] == password

@app.get("/")
def read_root(request: Request):
    # This is an example of passing dynamic content to the template.
    context = {"request": request, "name": "User"}
    return templates.TemplateResponse("index.html", context)

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if not verify_password(username, password):
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
def signup(username: str = Form(...), password: str = Form(...)):
    users = get_users()
    if username in users:
        return {"error": "Username already exists"}
    # Store the user in the JSON database
    users[username] = {"username": username, "password": password}
    save_users(users)
    return {"success": True}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
