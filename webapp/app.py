from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import database.database as db

WEB_DIR = os.path.join(os.path.dirname(__file__),"html")


app = FastAPI()

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