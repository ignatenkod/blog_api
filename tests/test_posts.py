import pytest
from httpx import AsyncClient
from app.core.security import create_access_token
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate

@pytest.mark.asyncio
async def test_create_post(async_client: AsyncClient, db_session):
    # Create a test user
    test_user = UserCreate(
        email="postuser@example.com",
        password="password",
        full_name="Post User"
    )
    db_user = await user.create(db_session, obj_in=test_user)
    
    # Create token
    token = create_access_token(data={"sub": db_user.email})
    
    # Create post
    post_data = PostCreate(
        title="Test Post",
        content="Test content",
        tag_ids=[]
    )
    response = await async_client.post(
        "/api/v1/posts/",
        json=post_data.dict(),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["author"]["email"] == "postuser@example.com"
