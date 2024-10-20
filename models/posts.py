from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    UserID: str
    Texto: str

class NewPost(BaseModel):
    AuthorID: int
    Texto: str
    MediaType: str
    MediaURL: Optional[str] = ""
    Caption: Optional[str] = ""

class GetPost(BaseModel):
    PostID: str

class LikePost(BaseModel):
    PostID: str