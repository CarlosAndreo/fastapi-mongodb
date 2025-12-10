from typing import Dict, Generator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.core.config import settings
from app.core.constants import API_PREFIX
from app.main import app

fake = Faker(locale="es_ES")


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """Clean all collections in database before each test.

    This fixture runs automatically before each test to ensure
    a clean database state. Uses sync pymongo client for compatibility.
    """
    client = MongoClient(settings.ME_CONFIG_MONGODB_URL)
    db = client[settings.MONGO_INITDB_DATABASE]
    collections = db.list_collection_names()
    for collection_name in collections:
        if not collection_name.startswith("system."):
            db[collection_name].delete_many({})
    client.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient for making API requests.

    Yields:
        TestClient: A FastAPI test client
    """
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="function")
def valid_user_data() -> Dict:
    """Provide valid user registration data using Faker.

    Returns:
        Dict: Valid user data for registration
    """
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(
            length=16, special_chars=True, digits=True, upper_case=True, lower_case=True
        ),
    }


@pytest.fixture(scope="function")
def registered_user(client, valid_user_data) -> Dict:
    """Register a user and return user data with credentials.

    Args:
        client: The test client fixture
        valid_user_data: Valid user data fixture

    Returns:
        Dict: User data including username and password
    """
    response = client.post(
        url=f"{API_PREFIX}/auth/register",
        json=valid_user_data,
    )
    assert response.status_code == 201, f"Registration failed: {response.json()}"
    return {
        **valid_user_data,
        **response.json(),
    }


@pytest.fixture(scope="function")
def user_token(client, registered_user) -> str:
    """Authenticate registered user and return access token.

    Args:
        client: The test client fixture
        registered_user: The registered user fixture

    Returns:
        str: JWT access token for the user
    """
    response = client.post(
        url=f"{API_PREFIX}/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, f"Login failed: {response.json()}"
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def authenticated_client(client, user_token) -> TestClient:
    """Provide a TestClient with user authentication headers.

    Args:
        client: The test client fixture
        user_token: The JWT token fixture

    Returns:
        TestClient: A test client with auth headers pre-configured
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {user_token}",
    }
    return client
