from pydantic import BaseModel
from typing import Optional, List
from bson.objectid import ObjectId

class Comment(BaseModel):
    UserID: str
    Texto: str
    Likes: List[str] = []

class PostComment(BaseModel):
    PostID: str
    UserID: str
    Texto: str
    Likes: List[str] = []

class NewPost(BaseModel):
    AuthorID: int
    Texto: str
    MediaType: str
    MediaURL: Optional[str] = ""
    Caption: Optional[str] = ""
    Likes: List[str] = []
    Comentarios: List[Comment] = []

class GetPost(BaseModel):
    PostID: str

class LikePost(BaseModel):
    PostID: str
    LikeAuthorID: str
    
class LikeComment(BaseModel):
    post_id: str
    comment_id: str
    user_id: str