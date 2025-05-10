from typing import Annotated, Generator
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from fastapi import Depends

# Create SQLite engine
DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

# Session dependency
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def create_all_tables(app):
    # Create tables on startup
    SQLModel.metadata.create_all(engine)
    yield
    # Optional: Cleanup on shutdown