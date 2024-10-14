from pydantic import BaseModel, Field
from typing import Optional, List

class Comment(BaseModel):
    UserID: str
    Texto: str


class NewDestination(BaseModel):
    _id: ObjectId = Field(alias="_id")
    AuthorID: str
    DestinationName: str
    Description: str
    Location: str
    Likes: List[str] = []
    Comentarios: List[Comment] = []


class BucketListCreation(BaseModel):
    _id: ObjectId = Field(alias="_id")
    AuthorID: str
    Destinos : List[DestinationID] = []
    #esto se debe de definir
    Likes: List[str] = []
    Comentarios: List[Comment] = []
    
class CreateTrip(BaseModel):
    _id: ObjectId = Field(alias="_id")
    Participants: List[str] = []
    Destinos: List[DestinationID] = []
    Likes: List[str] = []
    Comentarios: List[Comment] = []
    
