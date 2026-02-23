import jwt
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schema, model
from sqlmodel import Session
#It help in setting login before doing anything in the app
#SECRET_KEY
#ALGORITHM
#ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
   
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is  None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(model.get_session)  # FIX: get_session not init_db
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(model.User).filter(model.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception

    return user