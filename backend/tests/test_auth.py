"""Tests for authentication endpoints."""
import pytest
from httpx import AsyncClient


class TestSignup:
    """Test cases for user signup endpoint."""

    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient, test_user_data: dict):
        """Test successful user registration."""
        response = await client.post("/api/v1/auth/signup", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Account created successfully"
        assert "id" not in data  # No sensitive data in response

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient, test_user_data: dict):
        """Test signup with already registered email."""
        # First signup
        await client.post("/api/v1/auth/signup", json=test_user_data)

        # Second signup with same email
        response = await client.post("/api/v1/auth/signup", json=test_user_data)

        assert response.status_code == 400
        data = response.json()
        # Error format is {"error": {"message": "..."}}
        assert "Email already registered" in data.get("error", {}).get("message", "")

    @pytest.mark.asyncio
    async def test_signup_password_mismatch(self, client: AsyncClient):
        """Test signup with mismatched passwords."""
        signup_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "confirm_password": "DifferentPass456!",
        }

        response = await client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 400
        data = response.json()
        assert "Passwords do not match" in data.get("error", {}).get("message", "")

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client: AsyncClient):
        """Test signup with invalid email format."""
        signup_data = {
            "email": "not-an-email",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!",
        }

        response = await client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_signup_short_password(self, client: AsyncClient):
        """Test signup with password too short."""
        signup_data = {
            "email": "test@example.com",
            "password": "short",
            "confirm_password": "short",
        }

        response = await client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_signup_missing_fields(self, client: AsyncClient):
        """Test signup with missing required fields."""
        signup_data = {
            "email": "test@example.com",
            # Missing password and confirm_password
        }

        response = await client.post("/api/v1/auth/signup", json=signup_data)

        assert response.status_code == 422  # Validation error


class TestLogin:
    """Test cases for user login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user_data: dict, test_user_login: dict):
        """Test successful user login."""
        # First create the user
        await client.post("/api/v1/auth/signup", json=test_user_data)

        # Then login
        response = await client.post("/api/v1/auth/login", json=test_user_login)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user_data: dict):
        """Test login with wrong password."""
        # First create the user
        await client.post("/api/v1/auth/signup", json=test_user_data)

        # Then try to login with wrong password
        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword456!",
        }

        response = await client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data.get("error", {}).get("message", "")

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with email that doesn't exist."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SecurePass123!",
        }

        response = await client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data.get("error", {}).get("message", "")

    @pytest.mark.asyncio
    async def test_login_invalid_email_format(self, client: AsyncClient):
        """Test login with invalid email format."""
        login_data = {
            "email": "not-an-email",
            "password": "SecurePass123!",
        }

        response = await client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 422  # Validation error


class TestLogout:
    """Test cases for user logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_success(self, client: AsyncClient, test_user_data: dict, test_user_login: dict):
        """Test successful user logout."""
        # First create and login the user
        await client.post("/api/v1/auth/signup", json=test_user_data)
        login_response = await client.post("/api/v1/auth/login", json=test_user_login)
        access_token = login_response.json()["access_token"]

        # Then logout (requires authentication)
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.post("/api/v1/auth/logout", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "Logged out successfully" in data["message"]

    @pytest.mark.asyncio
    async def test_logout_without_auth(self, client: AsyncClient):
        """Test logout without authentication token."""
        response = await client.post("/api/v1/auth/logout")

        assert response.status_code == 403  # No credentials provided


class TestRefreshToken:
    """Test cases for token refresh endpoint."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client: AsyncClient, test_user_data: dict, test_user_login: dict):
        """Test successful token refresh."""
        # First create and login the user
        await client.post("/api/v1/auth/signup", json=test_user_data)
        login_response = await client.post("/api/v1/auth/login", json=test_user_login)
        refresh_token = login_response.json()["refresh_token"]

        # Then refresh the token
        refresh_data = {"refresh_token": refresh_token}
        response = await client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, client: AsyncClient):
        """Test refresh with invalid token."""
        refresh_data = {"refresh_token": "invalid_token"}
        response = await client.post("/api/v1/auth/refresh", json=refresh_data)

        assert response.status_code == 401


class TestGetMe:
    """Test cases for get current user endpoint."""

    @pytest.mark.asyncio
    async def test_get_me_success(self, client: AsyncClient, test_user_data: dict, test_user_login: dict):
        """Test getting current user profile."""
        # First create and login the user
        await client.post("/api/v1/auth/signup", json=test_user_data)
        login_response = await client.post("/api/v1/auth/login", json=test_user_login)
        access_token = login_response.json()["access_token"]

        # Then get current user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_get_me_without_token(self, client: AsyncClient):
        """Test getting current user without token."""
        response = await client.get("/api/v1/auth/me")

        assert response.status_code == 403  # No credentials provided

    @pytest.mark.asyncio
    async def test_get_me_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 401
