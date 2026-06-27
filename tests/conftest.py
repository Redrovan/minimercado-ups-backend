import os

# Define testing database URL BEFORE importing any app module
os.environ["DATABASE_URL"] = "sqlite:///./test_minimercado.db"

import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine, SessionLocal
from app.main import app
from app.utils.dependencies import get_db

@pytest.fixture(autouse=True)
def prepare_database():
    # Force close any existing connections to release Windows file lock
    engine.dispose()
    
    # Remove old test DB if it exists
    if os.path.exists("./test_minimercado.db"):
        try:
            os.remove("./test_minimercado.db")
        except Exception:
            pass
            
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up and release locks
    engine.dispose()
    if os.path.exists("./test_minimercado.db"):
        try:
            os.remove("./test_minimercado.db")
        except Exception:
            pass

@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    # Set raise_server_exceptions=False so unhandled errors return HTTP 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
