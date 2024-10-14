import os
import psycopg2
from enum import Enum
from passlib.context import CryptContext  # Importa para manejar el hashing de contraseñas
from pymongo import MongoClient
from typing import Optional, List
from bson import ObjectId

class ResultCode(Enum):
    SUCCESS = 0
    FAILED_TRANSACTION = 1
    REPEATED_ELEMENT = 2
    USER_NOT_FOUND = 3  # Añadido para el caso en que el usuario no sea encontrado
    INVALID_PASSWORD = 4  # Añadido para el caso en que la contraseña sea inválida

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
        )
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Contexto para manejar el hashing

    def register_user(self, user):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL AddUser(%s, %s, %s, %s)",
                (user.name, user.mail, user.password, user.role),
            )
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION
        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            return ResultCode.REPEATED_ELEMENT

    def delete_user(self, user):
        try:
            cursor = self.connection.cursor()
            cursor.execute("CALL DeleteUser(%s)", (user.mail,))
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION

    def edit_user(self, user):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL EditUser(%s, %s, %s, %s, %s)",
                (user.UserID, user.name, user.mail, user.password, user.role),
            )
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION

    def create_post(self, post):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL CreatePost(%s, %s, %s, %s, %s)",
                (
                    post.AuthorID,
                    post.Texto,
                    post.MediaType,
                    post.MediaURL,
                    post.Caption,
                ),
            )
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION

    def authenticate_user(self, username: str, password: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT password FROM users WHERE mail = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            
            if result is None:
                return ResultCode.USER_NOT_FOUND  # Usuario no encontrado
            
            hashed_password = result[0]
            if not self.pwd_context.verify(password, hashed_password):
                return ResultCode.INVALID_PASSWORD  # Contraseña inválida

            return ResultCode.SUCCESS  # Autenticación exitosa

        except psycopg2.errors.InFailedSqlTransaction:
            return ResultCode.FAILED_TRANSACTION

    def get_user_info(self, username: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name, role FROM users WHERE mail = %s", (username,))
            result = cursor.fetchone()
            cursor.close()

            if not result:
                return ResultCode.USER_NOT_FOUND
            return result

        except psycopg2.errors.InFailedSqlTransaction:
            return ResultCode.FAILED_TRANSACTION

class MongoDatabase:
    def __init__(self):
        self.client = MongoClient(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            authSource=os.environ.get("DB_NAME")
        )
        self.db = self.client[os.environ.get("DB_NAME")]
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def create_post(self, post):
        try:
            post_id = self.db.posts.insert_one(post.dict(by_alias=True)).inserted_id
            return post_id
        except Exception as e:
            return None
        