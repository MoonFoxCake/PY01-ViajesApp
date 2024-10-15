from fastapi import FastAPI, status, Response, Depends, HTTPException, Request  # Añadido 'Depends' y 'HTTPException' para manejar dependencias y errores
from db import Database, ResultCode, MongoDatabase
from models.NewPost import Comment, NewPost
from models.PostsMongo import NewPost
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
mdb = MongoDatabase()



@app.get("/")
async def get_version():
    return {"message": "Connection acknowledge"}

@app.post("/register")
async def register_user(user: NewUser):
    result = db.register_user(user)
    if result == ResultCode.SUCCESS:
        return {"message": "User registered successfully"}
    elif result == ResultCode.REPEATED_ELEMENT:
        return Response(status_code=status.HTTP_409_CONFLICT)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/deleteUser")
async def delete_user(user: DelUser):
    result = db.delete_user(user)
    if result == ResultCode.SUCCESS:
        return {"message": "User deleted successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/editUser")
async def edit_user(user: EditUser):
    result = db.edit_user(user)
    if result == ResultCode.SUCCESS:
        return {"message": "User edited successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/login")
async def authenticate_user(user: UserAuth):
    result = db.authenticate_user(user)
    if result == ResultCode.SUCCESS:
        return {"message": "User authenticated successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif result == ResultCode.INVALID_PASSWORD:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/posts")
async def create_post(post: NewPost):
    result = mdb.create_post(post)
    if result == ResultCode.SUCCESS:
        return {"message": "Post created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/posts/{post_id}")
async def get_post(post_id: str):
    result = mdb.get_post(post_id)
    if result:
        return result
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/posts/{post_id}/like")
async def like_post(post_id: str):
    result = mdb.like_post(post_id)
    if result == ResultCode.SUCCESS:
        return {"message": "Post liked successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/posts/{post_id}/comment")
async def add_comment(post_id: str, comment: Comment):
    result = mdb.add_comment(post_id, comment)
    if result == ResultCode.SUCCESS:
        return {"message": "Comment added successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
