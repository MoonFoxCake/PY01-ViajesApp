from fastapi import FastAPI, status, Response, Depends, HTTPException, Request  # Añadido 'Depends' y 'HTTPException' para manejar dependencias y errores
from db import Database, ResultCode
from models.NewPost import NewPost
from models.user import NewUser, DelUser, EditUser, UserAuth  # Añadido 'UserAuth' para manejar el login
from typing import Optional
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Añadido para manejar el esquema de autenticación OAuth2
from jose import JWTError, jwt  # Añadido para manejar la creación y verificación de tokens JWT
from datetime import datetime, timedelta, timezone  # Añadido para manejar la expiración de los tokens
from passlib.context import CryptContext  # Añadido para manejar el hashing de contraseñas
import os

app = FastAPI()
db = Database()

# Configuraciones para JWT
SECRET_KEY = os.environ.get("SECRET_KEY")  # Clave secreta para firmar el JWT, debería estar en una variable de entorno
ALGORITHM = "HS256"  # Algoritmo utilizado para firmar el JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token en minutos

# Contexto para el manejo de contraseñas (hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependencia para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # Verifica si la contraseña plana coincide con la hash

def get_password_hash(password):
    return pwd_context.hash(password)  # Genera el hash de una contraseña

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Usa timezone-aware datetime
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Usa timezone-aware datetime
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # Crea un token JWT con los datos de usuario y la expiración

def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("sub")
        role = decoded_token.get("role")
        expiration = decoded_token.get("exp")
        return {"username": username, 
                "role": role,
                "exp": expiration}
    except JWTError:
        raise Exception

@app.get("/")
async def get_version():
    return {"message": "Connection acknowledge"}

# Endpoint para autenticación de usuarios (login)
@app.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    request = db.authenticate_user(form_data.username, form_data.password)
    match request:
        case ResultCode.USER_NOT_FOUND:
            response.status_code=status.HTTP_404_NOT_FOUND
            return {"message": "User given was not found"}
        case ResultCode.INVALID_PASSWORD:
            response.status_code=status.HTTP_401_UNAUTHORIZED
            return {"message": "Invalid credentials"}
        case ResultCode.SUCCESS:

            user_info = db.get_user_info(form_data.username)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={
                    "user": form_data.username,
                    "role": user_info[1]
                }, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        
        case ResultCode.FAILED_TRANSACTION:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": "An internal error occurred"}

@app.post("/registerUser")
async def register_user(user: NewUser, response: Response):
    user.password = get_password_hash(user.password)  # Hashea la contraseña antes de almacenarla
    request = db.register_user(user)
    match request:
        case ResultCode.SUCCESS:
            return {"message": "User created successfully"}
        case ResultCode.FAILED_TRANSACTION:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": "An internal error occurred"}
        case ResultCode.REPEATED_ELEMENT:
            response.status_code = status.HTTP_409_CONFLICT
            return {"message": "This element already exists on the database."}

@app.post("/removeUser")
async def delete_user(DelUser: DelUser, response: Response, request: Request):

    token = request.headers["Authorization"]
    info = None
    try:
        info = decode_token(token)
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid token."}
    role = info["role"]

    if role != 2:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Not enough permission"}
    else:
        request = db.delete_user(DelUser)
        match request:
            case ResultCode.SUCCESS:
                return {"message": "User deleted successfully"}
            case ResultCode.FAILED_TRANSACTION:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"message": "An internal error occurred"}

@app.post("/editUser")
async def edit_user(EditUser: EditUser, response: Response, request: Request):

    token = request.headers["Authorization"]
    info = None
    try:
        info = decode_token(token)
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid token."}
    role = info["role"]

    if role != 2:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Not enough permission"}
    else:
        request = db.edit_user(EditUser)
        match request:
            case ResultCode.SUCCESS:
                return {"message": "Information edited successfully"}
            case ResultCode.FAILED_TRANSACTION:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"message": "An internal error occurred"}

@app.post("/createPost")
async def create_post(post: NewPost, response: Response):
    request = db.create_post(post)
    match request:
        case ResultCode.SUCCESS:
            return {"message": "Post created successfully"}
        case ResultCode.FAILED_TRANSACTION:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": "An internal error occurred"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
