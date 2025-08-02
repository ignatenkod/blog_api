from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.db.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate

class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Tag]:
        result = await db.execute(select(self.model).filter(self.model.name == name))
        return result.scalars().first()

tag = CRUDTag(Tag)
