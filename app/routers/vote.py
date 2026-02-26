from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from .. import schema,model,oauth2

router = APIRouter(
    prefix="/vote", tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(model.get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{vote.post_id} not found")
    vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has already voted on post {vote.post_id}")
        else:
            new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return{"message": "succes"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()  

            return{"message": "succes"} 

