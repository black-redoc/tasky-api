import os
import json

import pytest
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.settings.database import create_database, get_db
from src.projects.router import router
from src.projects.schemas import ProjectSchema
from src.projects.models import Project

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


def test_get_project_by_title(client):
    response = client.get("/projects/title_test")
    expected_status_code = 404
    assert response.status_code == expected_status_code


def test_read_projects(client):
    response = client.get("/projects/")
    expected_status_code = 200
    assert response.status_code == expected_status_code


def test_create_project(client):
    with patch(
        "src.projects.service.create_project",
        return_value=ProjectSchema(
            id=1, title="Test Project", description="Test Description", tasks=[]
        ),
    ):
        project_data = {"title": "Test Project", "description": "Test Description"}
        response = client.post("/projects/", json=project_data)
        expected_status_code = 201
        body = json.loads(response.content.decode("utf-8"))
        expected_title = "Test Project"
        assert response.status_code == expected_status_code
        assert body["title"] == expected_title


def test_update_project_with_unknown_project(client):
    project_data = {
        "title": "Updated Project",
        "description": "Updated Description",
        "id": 1,
    }
    response = client.put("/projects/", json=project_data)
    expected_status_code = 404
    assert response.status_code == expected_status_code


def test_update_project(client):
    with patch(
        "src.projects.service.update_project",
        return_value=Project(
            title="Updated Project", description="Updated Description", id=1, tasks=[]
        ),
    ):
        project_data = {
            "title": "Updated Project",
            "description": "Updated Description",
        }
        response = client.put("/projects/", json=project_data)
        body = json.loads(response.content.decode("utf-8"))
        expected_status_code = 200
        expected_title = "Updated Project"
        expected_description = "Updated Description"
        assert response.status_code == expected_status_code
        assert body["title"] == expected_title
        assert body["description"] == expected_description


def test_delete_project_with_unknown_project(client):
    project_id = 1  # Assuming project with ID 1 exists
    response = client.delete(f"/projects/{project_id}")
    expected_status_code = 404
    assert response.status_code == expected_status_code
