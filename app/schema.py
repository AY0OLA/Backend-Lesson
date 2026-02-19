from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    # title, content, published will be inherit from PostBase
   id: int