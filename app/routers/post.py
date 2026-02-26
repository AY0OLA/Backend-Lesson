from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
import time
from .. import schema, oauth2
from sqlmodel import Session, func
from ..model import Posts, get_session,Vote

router = APIRouter(
    prefix="/posts", tags=['Posts']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.PostOut])
def get_posts( db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    print(current_user)
    #to get the user post only
    #post = db.query(Posts).filter(Posts.owner_id == current_user.id).all()
    #to skip post we use offset(skip) and pass the skip pramameter i.e skip: int =0
    # post = db.query(Posts).filter(Posts.title.contains(search)).limit(limit).all()
    rows = (
        db.query(Posts, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Posts.id, isouter=True)
        .filter(Posts.title.contains(search))
        .group_by(Posts.id).filter(Posts.title.contains(search)).limit(limit).all()
    )

    post = [{"Post": post, "vote": votes} for post, votes in rows]
    return post



@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def create_posts(post: schema.CreatePost, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    new_post = Posts(owner_id =current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

 
@router.get("/{id}", response_model=schema.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_session),
    current_user=Depends(oauth2.get_current_user),
):
    # post = db.query(Posts).filter(Posts.id == id).first()
    row = (
        db.query(Posts, func.count(Vote.post_id).label("vote"))
        .join(Vote, Vote.post_id == Posts.id, isouter=True)
        .filter(Posts.id == id)
        .group_by(Posts.id)
        .first()
    )

    if row is None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")

    post, vote_count = row
    HTTPException(status_code=403, detail="Not authorized")

    return {"Post": post, "vote": vote_count}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user)
    post_query = db.query(Posts).filter(Posts.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
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
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    for key, value in update_post.dict().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
