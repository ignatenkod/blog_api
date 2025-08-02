import pytest
from httpx import AsyncClient
from app.core.security import get_password_hash
from app.crud.user import user
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, db_session):
    # Create a test user
    test_user = UserCreate(
        email="test@example.com",
        password="password",
        full_name="Test User"
    )
    await user.create(db_session, obj_in=test_user)
    
    # Test login
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
