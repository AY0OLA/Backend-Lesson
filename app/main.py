from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .model import Posts, get_session  # (Posts, get_session not used here yet)

app = FastAPI()

# Optional sha: create tables (only works if you really won use SQLModel engine wey Dey above)
# init_db()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
posts = [
    {"title": "tile of post 1", "content": "content of post 1", "id": 1},
    {"title": "favotire foods", "content": "I like pizza", "id": 2},
]

#DB Connection
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
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

@app.post("/")
def get_post(get_session):
    return {"data": Posts}


@app.get("/")
def get_user():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


# FIXES:
# - INSERT no Dey use WHERE
# - remove undefined "id"
# - column name gats match DB: published (not publish) unless say your DB Dey different
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """
        INSERT INTO posts (title, content, publish)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# FIX: must pass a 1-item tuple -> (id,)
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} doesn't exist",
        )

    return {"data": updated_post}