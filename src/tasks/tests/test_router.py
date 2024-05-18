import os
import json

import pytest
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.settings.database import create_database, get_db
from src.tasks.router import router
from src.tasks.schemas import TaskSchema
from src.tasks.models import Task

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    with TestClient(router) as client:
        yield client


@pytest.fixture
def mock_db_session():
    session = Session()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


app.dependency_overrides[get_db] = mock_db_session


@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: can be used to initialize the database
    create_database()

    yield  # this is where the testing happens

    # Teardown
    try:
        os.remove("test.db")
    except:
        """
        Do nothing
        """


def test_db():
    assert os.getenv("DATABASE_URL") == "sqlite:///./test.db"


def test_read_tasks(client):
    response = client.get("/tasks/")
    expected_status_code = 200
    assert response.status_code == expected_status_code


def test_create_task(client):
    with patch(
        "src.tasks.service.create_task",
        return_value=TaskSchema(
            id=1,
            title="Test task",
            description="Test Description",
            project_id=1,
            status="doing",
        ),
    ):
        task_data = {
            "title": "Test task",
            "description": "Test Description",
            "project_id": 1,
            "status": "doing",
        }
        response = client.post("/tasks/", json=task_data)
        expected_status_code = 201
        body = json.loads(response.content.decode("utf-8"))
        expected_title = "Test task"
        assert response.status_code == expected_status_code
        assert body["title"] == expected_title


def test_update_task_with_unknown_task(client):
    task_data = {
        "title": "Updated task",
        "description": "Updated Description",
        "id": 1,
        "project_id": 1,
        "status": "doing",
    }
    response = client.put("/tasks/", json=task_data)
    expected_status_code = 404
    assert response.status_code == expected_status_code


def test_update_task(client):
    with patch(
        "src.tasks.service.update_task",
        return_value=Task(
            title="Updated task",
            description="Updated Description",
            id=1,
            project_id=1,
            status="doing",
        ),
    ):
        task_data = {
            "title": "Updated task",
            "description": "Updated Description",
            "status": "done",
            "project_id": 1,
        }
        response = client.put("/tasks/", json=task_data)
        body = json.loads(response.content.decode("utf-8"))
        expected_status_code = 200
        expected_title = "Updated task"
        expected_description = "Updated Description"
        assert response.status_code == expected_status_code
        assert body["title"] == expected_title
        assert body["description"] == expected_description


def test_delete_task_with_unknown_task(client):
    task_id = 1
    response = client.delete(f"/tasks/{task_id}")
    expected_status_code = 404
    assert response.status_code == expected_status_code
