from pydantic import BaseModel, Field
from typing import Optional, List

class Comment(BaseModel):
    UserID: str
    Texto: str
    Likes: List[str] = []

class LikeDestination(BaseModel):
    PostID: str

class NewDestination(BaseModel):
    AuthorID: str
    DestinationName: str
    Description: str
    Location: str
    Likes: List[str] = []
    Comentarios: List[Comment] = []

class BucketListCreation(BaseModel):
    AuthorID: str
    Destinos : List[str] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []

class BucketListFollower(BaseModel):
    BucketListID: str
    FollowerUserID: str

class CreateTrip(BaseModel):
    Participants: List[str] = []
    Destinos: List[str] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []
    
