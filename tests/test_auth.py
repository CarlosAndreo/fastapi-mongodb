from faker import Faker

from app.core.constants import API_PREFIX
from app.core.jwt import create_access_token, create_refresh_token

fake = Faker(locale="es_ES")

# Endpoint paths
register = f"{API_PREFIX}/auth/register"
login = f"{API_PREFIX}/auth/login"
refresh = f"{API_PREFIX}/auth/refresh"


# ============================================================================
# REGISTRATION TESTS
# ============================================================================


def test_register_success(client, valid_user_data):
    """Test successful user registration.

    Verifies:
    - Registration returns 201 status
    - Response contains username and email
    - Password is not returned in response
    """
    response = client.post(url=register, json=valid_user_data)
    data = response.json()
    assert response.status_code == 201, f"Error: {data}"
    assert data["username"] == valid_user_data["username"]
    assert data["email"] == valid_user_data["email"]
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client, valid_user_data):
    """Test registering with duplicate username.

    Verifies:
    - Cannot create two users with same username
    - Returns 400 Bad Request
    """
    first_response = client.post(url=register, json=valid_user_data)
    assert first_response.status_code == 201

    duplicate_response = client.post(url=register, json=valid_user_data)
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"]


def test_register_invalid_email(client, valid_user_data):
    """Test registration with invalid email format.

    Verifies:
    - Returns 422 for invalid email format
    """
    invalid_data = {**valid_user_data, "email": "invalid-email"}
    response = client.post(url=register, json=invalid_data)
    assert response.status_code == 422


def test_register_missing_password(client):
    """Test registration with missing password.

    Verifies:
    - Returns 422 when password is missing
    """
    response = client.post(
        url=register,
        json={
            "username": fake.user_name(),
            "email": fake.email(),
        },
    )
    assert response.status_code == 422


def test_register_missing_username(client):
    """Test registration with missing username.

    Verifies:
    - Returns 422 when username is missing
    """
    response = client.post(
        url=register,
        json={
            "email": fake.email(),
            "password": fake.password(),
        },
    )
    assert response.status_code == 422


def test_register_without_email(client):
    """Test registration without optional email field.

    Verifies:
    - Can register successfully without email (email is optional)
    """
    response = client.post(
        url=register,
        json={
            "username": fake.user_name(),
            "password": fake.password(),
        },
    )
    assert response.status_code == 201


# ============================================================================
# LOGIN TESTS
# ============================================================================


def test_login_success(client, registered_user):
    """Test successful user login.

    Verifies:
    - Login returns 200 status
    - Response contains access_token, refresh_token, and token_type
    """
    response = client.post(
        url=login,
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    data = response.json()
    assert response.status_code == 200, f"Error: {data}"
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_username(client):
    """Test login with non-existent username.

    Verifies:
    - Returns 401 for non-existent user
    """
    response = client.post(
        url=login,
        data={
            "username": fake.user_name(),
            "password": fake.password(),
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_invalid_password(client, registered_user):
    """Test login with incorrect password.

    Verifies:
    - Returns 401 for invalid password
    """
    response = client.post(
        url=login,
        data={
            "username": registered_user["username"],
            "password": fake.password(),
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_missing_credentials(client):
    """Test login with missing credentials.

    Verifies:
    - Returns 422 when credentials are missing
    """
    response = client.post(url=login, data={})
    assert response.status_code == 422


# ============================================================================
# TOKEN REFRESH TESTS
# ============================================================================


def test_refresh_success(client, registered_user):
    """Test successful token refresh.

    Verifies:
    - Can refresh token with valid refresh_token
    - Returns new access_token and refresh_token
    """
    login_response = client.post(
        url=login,
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post(
        url=refresh,
        json={"refresh_token": refresh_token},
    )
    data = refresh_response.json()
    assert refresh_response.status_code == 200, f"Error: {data}"
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_invalid_token(client):
    """Test token refresh with access token instead of refresh token.

    Verifies:
    - Returns 401 when using wrong token type
    """
    access_token = create_access_token(data={"sub": fake.user_name()})
    response = client.post(
        url=refresh,
        json={"refresh_token": access_token},
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_refresh_nonexistent_user(client):
    """Test token refresh with token for non-existent user.

    Verifies:
    - Returns 404 when user in token doesn't exist
    """
    fake_username = fake.user_name()
    fake_refresh_token = create_refresh_token(data={"sub": fake_username})
    response = client.post(
        url=refresh,
        json={"refresh_token": fake_refresh_token},
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_refresh_missing_token(client):
    """Test token refresh without providing token.

    Verifies:
    - Returns 422 when refresh_token is missing
    """
    response = client.post(url=refresh, json={})
    assert response.status_code == 422


# ============================================================================
# AUTHORIZATION TESTS
# ============================================================================


def test_token_contains_correct_username(client, registered_user):
    """Test that token contains correct user information.

    Verifies:
    - Token can be used to authenticate
    - Authenticated endpoint returns correct user
    """
    login_response = client.post(
        url=login,
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    token = login_response.json()["access_token"]
    me_response = client.get(
        url=f"{API_PREFIX}/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == registered_user["username"]
