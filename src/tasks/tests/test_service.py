import os
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from sqlalchemy.orm import Session
from src.settings.database import create_database, get_db
from src.tasks import service, schemas
from src.tasks.router import router


app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    with TestClient(router) as client:
        yield client


@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)


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


def test_get_tasks(mock_db_session):
    tasks = service.get_tasks(mock_db_session, skip=0, limit=10)
    assert tasks is not None


def test_create_task(mock_db_session):
    task_data = schemas.TaskSchema(
        title="Test task", description="Test Description", status="doing", project_id=1
    )
    created_task = service.create_task(mock_db_session, task_data)
    assert created_task is not None


def test_create_task_with_exception(mock_db_session):
    task_data = None
    response_exception = service.create_task(mock_db_session, task_data)
    response_exception = json.loads(response_exception.body.decode("utf-8"))
    assert "error" in response_exception


def test_delete_task(mock_db_session):
    task_id = 1  # Assuming task with ID 1 exists
    response = service.delete_task(mock_db_session, task_id)
    assert response.status_code == 200


def test_update_task(mock_db_session):
    task_data = schemas.TaskSchema(
        id=1,
        title="Updated Task",
        description="Updated Description",
        status="doing",
        project_id=1,
    )
    updated_task = service.update_task(mock_db_session, task_data)
    assert updated_task is not None


def test_update_task_with_exception(mock_db_session):
    task_data = None
    response_exception = service.update_task(mock_db_session, task_data)
    response_exception = response_exception.body.decode("utf-8")
    assert "error" in response_exception
