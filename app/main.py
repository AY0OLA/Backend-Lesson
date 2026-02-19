from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import time
from . import schema
from sqlmodel import Session
from .model import init_db, Posts, get_session

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


@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}

    db_post = Posts(
        title=post.title,
        content=post.content,
        published=post.published
    )
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schema.Post])
def get_posts( db: Session = Depends(get_session)):
    post = db.query(Posts).all()
    return post



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.CreatePost, db: Session = Depends(get_session)):
    new_post = Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int,  db: Session = Depends(get_session)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_session)):
    post = db.query(Posts).filter(Posts.id == id)
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def update_post(id: int,update_post: schema.CreatePost, db: Session = Depends(get_session)):
    post_update = db.query(Posts).filter(Posts.id == id)
    post = post_update.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} doesn't exist")
    post_update.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_update.first()