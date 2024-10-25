from pydantic import BaseModel, Field
from typing import Optional, List

class Comment(BaseModel):
    UserID: str
    Texto: str

class LikeDestination(BaseModel):
    PostID: str

class NewDestination(BaseModel):
    AuthorID: str
    DestinationName: str
    Description: str
    Location: str
    Likes: List[str] = [] # No debería ser un integer?
    Comentarios: List[Comment] = []

class BucketListCreation(BaseModel):
    AuthorID: str
    Destinos : List[str] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []

class CreateTrip(BaseModel):
    Participants: List[str] = []
    Destinos: List[str] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []
    
