
import fastapi
from fastapi.responses import FileResponse
import os
import api.api

app = fastapi.FastAPI()
app.include_router(api.api.router)

WEB_DIR = os.path.join(os.path.dirname(__file__), "html")

@app.get("/")
def index_page():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))

@app.get("/login")
def login_page():
    return FileResponse(os.path.join(WEB_DIR, "login.html"))

@app.get("/signup")
def signup_page():
    return FileResponse(os.path.join(WEB_DIR, "signup.html"))

@app.get("/dashboard")
def dashboard_page():
    return FileResponse(os.path.join(WEB_DIR, "dashboard.html"))

@app.on_event("startup")
def on_startup():
    from database.database import init_data
    init_data()  # Call the function to initialize the database on startup