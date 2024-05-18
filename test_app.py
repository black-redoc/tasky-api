import pytest
from fastapi.testclient import TestClient
from src.settings.database import engine

from app import app


@pytest.fixture
def client():

    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_db_session():
    session = engine.connect()
    yield session
    session.close()


def test_db_session_middleware(mock_db_session):
    # Test the database session middleware
    assert mock_db_session is not None


def test_task_router(client):
    # Test the task router
    response = client.get("/tasks/")
    assert response.status_code == 200


def test_project_router(client):
    # Test the project router
    response = client.get("/projects/")
    assert response.status_code == 200
