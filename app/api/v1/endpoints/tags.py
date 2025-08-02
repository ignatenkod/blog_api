from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud.tag import tag
from app.db.session import get_db
from app.schemas.tag import Tag, TagCreate, TagUpdate
from app.core.security import get_current_active_superuser

router = APIRouter()

@router.get("/", response_model=List[Tag])
async def read_tags(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return await tag.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Tag)
async def create_tag(
    *,
    db: AsyncSession = Depends(get_db),
    tag_in: TagCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    db_tag = await tag.get_by_name(db, name=tag_in.name)
    if db_tag:
        raise HTTPException(
            status_code=400,
            detail="The tag with this name already exists.",
        )
    return await tag.create(db, obj_in=tag_in)

@router.get("/{tag_id}", response_model=Tag)
async def read_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_tag = await tag.get(db, id=tag_id)
    if not db_tag:
        raise HTTPException(
            status_code=404,
            detail="The tag with this id does not exist.",
        )
    return db_tag

@router.put("/{tag_id}", response_model=Tag)
async def update_tag(
    *,
    db: AsyncSession = Depends(get_db),
    tag_id: int,
    tag_in: TagUpdate,
    current_user: User = Depends(get_current_active_superuser),
):
    db_tag = await tag.get(db, id=tag_id)
    if not db_tag:
        raise HTTPException(
            status_code=404,
            detail="The tag with this id does not exist.",
        )
    return await tag.update(db, db_obj=db_tag, obj_in=tag_in)

@router.delete("/{tag_id}", response_model=Tag)
async def delete_tag(
    *,
    db: AsyncSession = Depends(get_db),
    tag_id: int,
    current_user: User = Depends(get_current_active_superuser),
):
    db_tag = await tag.get(db, id=tag_id)
    if not db_tag:
        raise HTTPException(
            status_code=404,
            detail="The tag with this id does not exist.",
        )
    return await tag.remove(db, id=tag_id)
