from pydantic import BaseModel, Field
from typing import Optional, List

class Comment(BaseModel):
    UserID: str
    Texto: str


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
    
class CreateTrip(BaseModel):
    Participants: List[str] = []
    Destinos: List[str] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []
    
