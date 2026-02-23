from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import time
from .. import schema, oauth2
from sqlmodel import Session
from ..model import Posts, get_session

router = APIRouter(
    prefix="/posts", tags=['Posts']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.Post])
def get_posts( db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    post = db.query(Posts).all()
    return post



@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.CreatePost, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    new_post = Posts(owner_id =current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schema.Post)
def get_post(id: int,  db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    post = db.query(Posts).filter(Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user)
    post_query = db.query(Posts).filter(Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int,update_post: schema.CreatePost,db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user)
    post = db.query(Posts).filter(Posts.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} doesn't exist")
    
    if post.owner_id != current_user.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    for key, value in update_post.dict().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
