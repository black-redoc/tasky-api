import os
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from sqlalchemy.orm import Session
from src.settings.database import create_database, get_db
from src.users import service, schemas
from src.users.router import router


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


def test_validate_user(mock_db_session):
    username = "test_username"
    tasks = service.validate_user(mock_db_session, username)
    assert tasks is not None


def test_login(mock_db_session):
    user = schemas.UserSchema(
        username="test_username", email="test_email@email.com", password="test_password"
    )
    tasks = service.login(mock_db_session, user)
    assert tasks is not None
