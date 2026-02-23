from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, ForeignKey


class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=False, nullable=False)
    owner_id: int = Field(index=True,foreign_key= "user.id", ondelete= "CASCADE", nullable= False)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(index=True, nullable=False)
    created_at: datetime = Field(index=True,default_factory=datetime.now,nullable=False)

# Postgres URL
database_url = "postgresql+psycopg2://postgres:Okunowo02@localhost:5432/Fastapi"
engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:  # use engine
        yield session