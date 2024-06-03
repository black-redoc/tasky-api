import os
import json

import pytest
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.settings.database import create_database, get_db
from src.users.router import router
from src.users.schemas import UserSchema
from src.users.models import User

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


def test_validate_user(client):
    with patch(
        "src.users.service.validate_user",
        return_value=JSONResponse(content={"is_valid_user": True}),
    ):
        response = client.post(
            "/users/",
            json={"email": "test@example.com", "password": "test_password"},
        )
        expected_status_code = 200
        assert response.content == b'{"is_valid_user":true}'
        assert response.status_code == expected_status_code


def test_login(client):
    with patch(
        "src.users.service.login", return_value=JSONResponse(content={"success": True})
    ):
        response = client.post(
            "/login/", json={"email": "email@example.com", "password": "test_password"}
        )
        expected_status_code = 200
        assert response.status_code == expected_status_code
        assert response.content == b'{"success":true}'
