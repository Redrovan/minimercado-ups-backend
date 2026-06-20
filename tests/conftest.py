import os

import pytest
from fastapi.testclient import TestClient

from app.database import Base
from app.database import SessionLocal
from app.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
