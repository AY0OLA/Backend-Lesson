from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from ..model import get_session, User
from .. import schema, utils, oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):

    user_login = db.query(User).filter(User.email == user_credentials.username).first()

    if not user_login:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invaild Credentials")

    if not utils.verify(user_credentials.password, user_login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invaild Credential")
    
    access_token = oauth2.create_access_token(data= {"user_id": user_login.id})

    return {"access_token": access_token, "token_type": "bearer"} 