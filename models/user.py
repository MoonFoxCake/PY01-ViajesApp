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
    UserID: int
    name: Optional[str] = None
    mail: Optional[str] = None
    password: Optional[str] = None
    role: Optional[int] = None

# Nueva clase para manejar la autenticación de usuarios
class UserAuth(BaseModel):
    username: str  # Nombre de usuario o correo electrónico que será utilizado para la autenticación
    password: str  # Contraseña del usuario para la autenticación
