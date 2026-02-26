from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    # title, content, published will be inherit from PostBase
   id: int
   created_at: datetime
   owner_id: int
   user: UserOut

class PostOut(BaseModel):
    Post: Post
    vote: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]