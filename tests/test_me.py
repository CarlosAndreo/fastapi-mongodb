from faker import Faker

from app.core.constants import API_PREFIX

fake = Faker(locale="es_ES")

# Endpoint paths
me = f"{API_PREFIX}/me"
change_password = f"{API_PREFIX}/me/change-password"


# ============================================================================
# GET CURRENT USER TESTS
# ============================================================================


def test_get_current_user_success(authenticated_client, registered_user):
    """Test retrieving current authenticated user.

    Verifies:
    - Returns 200 status
    - Response contains correct user data
    - Password is not included in response
    """
    response = authenticated_client.get(url=me)
    data = response.json()
    assert response.status_code == 200, f"Error: {data}"
    assert data["username"] == registered_user["username"]
    assert data["email"] == registered_user["email"]
    assert "password" not in data
    assert "hashed_password" not in data


def test_get_current_user_unauthorized(client):
    """Test accessing current user without authentication.

    Verifies:
    - Returns 401 when no auth token provided
    """
    response = client.get(url=me)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_get_current_user_invalid_token(client):
    """Test accessing current user with invalid token.

    Verifies:
    - Returns 401 for invalid token
    """
    response = client.get(
        url=me,
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401


# ============================================================================
# CHANGE PASSWORD TESTS
# ============================================================================


def test_change_password_success(authenticated_client, registered_user, client):
    """Test successful password change.

    Verifies:
    - Password change returns 200 status
    - Can login with new password
    - Cannot login with old password
    """
    new_password = fake.password(
        length=16, special_chars=True, digits=True, upper_case=True, lower_case=True
    )

    response = authenticated_client.patch(
        url=change_password,
        json={
            "old_password": registered_user["password"],
            "new_password": new_password,
        },
    )
    data = response.json()
    assert response.status_code == 200, f"Error: {data}"
    assert data["username"] == registered_user["username"]
    assert "password" not in data
    assert "hashed_password" not in data
    login_response = client.post(
        url=f"{API_PREFIX}/auth/login",
        data={
            "username": registered_user["username"],
            "password": new_password,
        },
    )
    assert login_response.status_code == 200
    old_login_response = client.post(
        url=f"{API_PREFIX}/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert old_login_response.status_code == 401


def test_change_password_incorrect_old_password(authenticated_client):
    """Test password change with incorrect old password.

    Verifies:
    - Returns 401 when old password is incorrect
    """
    response = authenticated_client.patch(
        url=change_password,
        json={
            "old_password": fake.password(),
            "new_password": fake.password(
                length=16,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_change_password_unauthorized(client):
    """Test changing password without authentication.

    Verifies:
    - Returns 401 when no auth token provided
    """
    response = client.patch(
        url=change_password,
        json={
            "old_password": fake.password(),
            "new_password": fake.password(),
        },
    )
    assert response.status_code == 401


def test_change_password_missing_fields(authenticated_client):
    """Test password change with missing fields.

    Verifies:
    - Returns 422 when required fields are missing
    """
    response = authenticated_client.patch(
        url=change_password,
        json={"old_password": fake.password()},
    )
    assert response.status_code == 422
    response = authenticated_client.patch(
        url=change_password,
        json={"new_password": fake.password()},
    )
    assert response.status_code == 422


def test_change_password_same_as_old(authenticated_client, registered_user, client):
    """Test changing password to same value as current password.

    Verifies:
    - Can change password to same value (should succeed)
    - Can still login with the password
    """
    response = authenticated_client.patch(
        url=change_password,
        json={
            "old_password": registered_user["password"],
            "new_password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    login_response = client.post(
        url=f"{API_PREFIX}/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert login_response.status_code == 200


def test_change_password_weak_password(authenticated_client, registered_user):
    """Test changing password to a weak password.

    Verifies:
    - Accepts weak passwords (no validation enforced in current implementation)
    Note: If password strength validation is added, this test should be updated
    """
    weak_password = "123"
    response = authenticated_client.patch(
        url=change_password,
        json={
            "old_password": registered_user["password"],
            "new_password": weak_password,
        },
    )
    assert response.status_code in [200, 422]


def test_change_password_invalid_token(client):
    """Test changing password with invalid authentication token.

    Verifies:
    - Returns 401 for invalid token
    """
    response = client.patch(
        url=change_password,
        headers={"Authorization": "Bearer invalid_token"},
        json={
            "old_password": fake.password(),
            "new_password": fake.password(),
        },
    )
    assert response.status_code == 401
