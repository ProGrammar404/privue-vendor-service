import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app as fastapi_app
from app.core.database import get_session

# Shared SQLite file DB for test session
TEST_DB_URL = "sqlite:///./test_db.sqlite"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False}
)

def get_test_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    # Clean DB for each test
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    fastapi_app.dependency_overrides[get_session] = get_test_session

    with TestClient(fastapi_app) as c:
        yield c

    # Reset overrides
    fastapi_app.dependency_overrides.clear()
