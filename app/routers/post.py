from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import time
from .. import schema
from sqlmodel import Session
from ..model import Posts, get_session

router = APIRouter()

@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schema.Post])
def get_posts( db: Session = Depends(get_session)):
    post = db.query(Posts).all()
    return post



@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.CreatePost, db: Session = Depends(get_session)):
    new_post = Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int,  db: Session = Depends(get_session)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_session)):
    post = db.query(Posts).filter(Posts.id == id)
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int,update_post: schema.CreatePost,db: Session = Depends(get_session)):
    post = db.query(Posts).filter(Posts.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} doesn't exist")

    for key, value in update_post.dict().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
