from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.post import post
from app.crud.user import user
from app.db.session import get_db
from app.schemas.post import Post, PostCreate, PostUpdate
from app.core.security import get_current_active_user
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Post])
async def read_posts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tag_id: Optional[int] = None,
):
    return await post.get_multi_with_filters(db, skip=skip, limit=limit, tag_id=tag_id)

@router.post("/", response_model=Post)
async def create_post(
    *,
    db: AsyncSession = Depends(get_db),
    post_in: PostCreate,
    current_user: User = Depends(get_current_active_user),
):
    return await post.create_with_tags(
        db, obj_in=post_in, author_id=current_user.id, tag_ids=post_in.tag_ids
    )

@router.get("/{post_id}", response_model=Post)
async def read_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_post = await post.get(db, id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="The post with this id does not exist.",
        )
    return db_post

@router.put("/{post_id}", response_model=Post)
async def update_post(
    *,
    db: AsyncSession = Depends(get_db),
    post_id: int,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_post = await post.get(db, id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="The post with this id does not exist.",
        )
    if db_post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own posts.",
        )
    return await post.update_with_tags(db, db_obj=db_post, obj_in=post_in)

@router.delete("/{post_id}", response_model=Post)
async def delete_post(
    *,
    db: AsyncSession = Depends(get_db),
    post_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_post = await post.get(db, id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="The post with this id does not exist.",
        )
    if db_post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts.",
        )
    return await post.remove(db, id=post_id)
