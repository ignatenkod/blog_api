from pydantic import BaseModel
from app.schemas.post import Post

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class Tag(TagBase):
    id: int
    posts: list[Post] = []
    
    class Config:
        orm_mode = True
