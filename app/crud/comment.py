from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.db.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_multi_by_post(
        self, db: AsyncSession, *, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

comment = CRUDComment(Comment)
