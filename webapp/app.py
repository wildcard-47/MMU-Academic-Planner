from fastapi import FastAPI
import database.database as db
from auth.api import router as auth_router
from member1_subjects.routes import router as subjects_router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="dev-secret-key")

app.include_router(auth_router)
app.include_router(subjects_router)


@app.on_event("startup")
async def startup_event():
    print("Starting up the FastAPI application...")
    db.init_data()


@app.get("/")
async def root():
    return {"message": "MMU Academic Planner API is running"}