from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.crud.base import CRUDBase
from app.db.models.post import Post, post_tag
from app.db.models.tag import Tag
from app.schemas.post import PostCreate, PostUpdate

class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def get_multi_by_author(
        self, db: AsyncSession, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_with_tags(
        self, db: AsyncSession, *, obj_in: PostCreate, author_id: int, tag_ids: List[int] = None
    ) -> Post:
        db_obj = Post(
            title=obj_in.title,
            content=obj_in.content,
            author_id=author_id,
        )
        if tag_ids:
            tags = await db.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
            db_obj.tags.extend(tags.scalars().all())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_with_tags(
        self, db: AsyncSession, *, db_obj: Post, obj_in: PostUpdate
    ) -> Post:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if "tag_ids" in update_data:
            tag_ids = update_data.pop("tag_ids")
            # Clear existing tags
            await db.execute(
                post_tag.delete().where(post_tag.c.post_id == db_obj.id)
            )
            # Add new tags
            if tag_ids:
                tags = await db.execute(select(Tag).filter(Tag.id.in_(tag_ids)))
                db_obj.tags.extend(tags.scalars().all())
        
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_multi_with_filters(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, tag_id: int = None
    ) -> List[Post]:
        query = select(self.model)
        if tag_id:
            query = query.join(self.model.tags).filter(Tag.id == tag_id)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

post = CRUDPost(Post)
