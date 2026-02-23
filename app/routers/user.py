from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
import time
from .. import schema, utils, oauth2
from sqlmodel import Session
from ..model import User, get_session

router = APIRouter(
    prefix= "/users",tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_session)):
    pwd_context = utils.hash(user.password)
    user.password = pwd_context
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_session),current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with {id} does not exist")
    
    return user