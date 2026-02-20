from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine


class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, index=True, nullable=False)

# Postgres URL
database_url = "postgresql+psycopg2://postgres:Okunowo02@localhost:5432/Fastapi"
engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:  # use engine
        yield session