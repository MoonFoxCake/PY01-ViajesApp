from pydantic import BaseModel
from typing import Optional

class NewUser(BaseModel):
    name: str
    mail: str
    password: str
    role: int

class DelUser(BaseModel):
    mail: str

class EditUser(BaseModel):
    mail: str
    name: Optional[str] = None
    newMail: Optional[str] = None
    password: Optional[str] = None
    role: Optional[int] = None
