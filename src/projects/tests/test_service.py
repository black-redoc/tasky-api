import os
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from sqlalchemy.orm import Session
from src.settings.database import create_database, get_db
from src.projects import service, schemas
from src.projects.router import router


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


def test_get_projects(mock_db_session):
    projects = service.get_projects(mock_db_session, skip=0, limit=10)
    assert projects is not None


def test_get_project_by_title(mock_db_session):
    projects = service.get_project_by_title(mock_db_session, title="title1")
    assert projects is not None


def test_create_project(mock_db_session):
    project_data = schemas.ProjectSchema(
        title="Test Project", description="Test Description"
    )
    created_project = service.create_project(mock_db_session, project_data)
    assert created_project is not None


def test_create_project_with_exception(mock_db_session):
    project_data = None
    response_exception = service.create_project(mock_db_session, project_data)
    response_exception = json.loads(response_exception.body.decode("utf-8"))
    assert "error" in response_exception


def test_delete_project(mock_db_session):
    project_id = 1  # Assuming project with ID 1 exists
    response = service.delete_project(mock_db_session, project_id)
    assert response.status_code == 200


def test_update_project(mock_db_session):
    project_data = schemas.ProjectSchema(
        id=1, title="Updated Project", description="Updated Description"
    )
    updated_project = service.update_project(mock_db_session, project_data)
    assert updated_project is not None


def test_update_project_with_exception(mock_db_session):
    project_data = None
    response_exception = service.update_project(mock_db_session, project_data)
    response_exception = response_exception.body.decode("utf-8")
    assert "error" in response_exception
