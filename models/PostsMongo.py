from pydantic import BaseModel, Field
from typing import Optional, List

class Comment(BaseModel):
    UserID: str
    Texto: str

class NewPost(BaseModel):
    AuthorID: str
    Texto: Optional[str] = None
    MediaURL: Optional[str] = None
    Likes: List[str] = []
    Comentarios: List[Comment] = []
