from fastapi import FastAPI
# from .model import init_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["https://backend-lesson-wjxo.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically when app starts
# @app.on_event("startup")
# def on_startup():
#     init_db()

#ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "World War loading"}