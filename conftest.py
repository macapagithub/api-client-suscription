import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from main import app

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, 
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

@pytest.fixture(name="session")
def session_fixture():
    """Create a new database session for a test."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a new FastAPI test client."""
    # def override_get_session():
    #     return session
    # app.dependency_overrides[Session] = override_get_session
    app.dependency_overrides[Session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()