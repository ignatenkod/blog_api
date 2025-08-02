from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.comment import comment
from app.crud.user import user
from app.db.session import get_db
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.core.security import get_current_active_user
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Comment])
async def read_comments(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    post_id: int = None,
):
    if post_id:
        return await comment.get_multi_by_post(db, post_id=post_id, skip=skip, limit=limit)
    return await comment.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Comment)
async def create_comment(
    *,
    db: AsyncSession = Depends(get_db),
    comment_in: CommentCreate,
    post_id: int,
    current_user: User = Depends(get_current_active_user),
):
    comment_in.post_id = post_id
    return await comment.create(db, obj_in=comment_in)

@router.get("/{comment_id}", response_model=Comment)
async def read_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_comment = await comment.get(db, id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="The comment with this id does not exist.",
        )
    return db_comment

@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    *,
    db: AsyncSession = Depends(get_db),
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_comment = await comment.get(db, id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="The comment with this id does not exist.",
        )
    if db_comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own comments.",
        )
    return await comment.update(db, db_obj=db_comment, obj_in=comment_in)

@router.delete("/{comment_id}", response_model=Comment)
async def delete_comment(
    *,
    db: AsyncSession = Depends(get_db),
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_comment = await comment.get(db, id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="The comment with this id does not exist.",
        )
    if db_comment.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments.",
        )
    return await comment.remove(db, id=comment_id)
