from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, ForeignKey, Relationship
from typing import Optional,List
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from .config import settings

# DB Connection (psycopg2)
# while True:
#     try:
#         conn = psycopg2.connect(
#             host={settings.database_hostname},
#             port={settings.database_port},
#             database={settings.database_name},
#             user={settings.database_username},
#             password={settings. database_password},
#             cursor_factory=RealDictCursor,
#             connect_timeout=3,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error:", error)
#         time.sleep(2)

class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=False, nullable=False)
    owner_id: int = Field(index=True,foreign_key= "user.id", ondelete= "CASCADE", nullable= False)
    user: List["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(index=True, nullable=False)
    created_at: datetime = Field(index=True,default_factory=datetime.now,nullable=False)
    posts: Optional[Posts] = Relationship(back_populates="user")

class Vote(SQLModel, table=True):
    post_id: int = Field(index=True,foreign_key= "posts.id", ondelete= "CASCADE", nullable= False, primary_key=True)
    user_id: int = Field(index=True,foreign_key= "user.id", ondelete= "CASCADE", nullable= False, primary_key=True)


# Postgres URL
database_url = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:  # use engine
        yield session