from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import database.database as db
from auth.api import router as auth_router
from dashboard.api import router as dashboard_router
from starlette.middleware.sessions import SessionMiddleware

WEB_DIR = os.path.join(os.path.dirname(__file__),"html")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


#include the auth router for handling authentication-related routes (login and signup)
app.include_router(auth_router)

#include the dashboard router for handling dashboard-related routes
app.include_router(dashboard_router)

#mount the static files directory for serving HTML files
app.mount("/html", StaticFiles(directory="html"), name="html")

@app.on_event("startup")
async def startup_event():
    print("Starting up the FastAPI application...")
    db.init_data()

@app.get("/")
async def main():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))

@app.get("/login")
async def main():
    return FileResponse(os.path.join(WEB_DIR, "login.html"))


@app.get("/signup")
async def main():
    return FileResponse(os.path.join(WEB_DIR, "signup.html"))


@app.get("/dashboard")
async def main():
    return FileResponse(os.path.join(WEB_DIR, "dashboard.html"))