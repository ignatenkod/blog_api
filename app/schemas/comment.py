from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import User

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class Comment(CommentBase):
    id: int
    author: User
    created_at: datetime
    
    class Config:
        orm_mode = True
