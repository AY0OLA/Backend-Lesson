from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine


class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  #typo fix


#FIX: no Dey mix sqlite and postgresql in one URL.
# Pick ONE.

# Option A: either you use SQLite (it Dey simple and it make sense for learning)
database_url = "sqlite:///postgres:Okunowo02@localhost/Fastapi"

# Option B: Postgres (use this one if you won actually use Postgres)
# database_url = "postgresql+psycopg2://postgres:Okunowo02@localhost/Fastapi"

engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(init_db) as session:
        yield session