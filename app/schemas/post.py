from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.user import User
from app.schemas.comment import Comment
from app.schemas.tag import Tag

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    tag_ids: Optional[List[int]] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class Post(PostBase):
    id: int
    author: User
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[Comment] = []
    tags: List[Tag] = []
    
    class Config:
        orm_mode = True
