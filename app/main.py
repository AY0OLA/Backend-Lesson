from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import time
from . import schema, utils
from sqlmodel import Session
from .model import init_db, Posts, get_session, User
from .routers import post, user


app = FastAPI()

# Create tables automatically when app starts
@app.on_event("startup")
def on_startup():
    init_db()



# DB Connection (psycopg2)
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="Fastapi",
            user="postgres",
            password="Okunowo02",
            cursor_factory=RealDictCursor,
            connect_timeout=3,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)