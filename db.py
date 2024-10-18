import os
import psycopg2
import pymongo
import redis
import models.user
import models
from enum import Enum

class ResultCode(Enum):
    SUCCESS = 0
    FAILED_TRANSACTION = 1
    REPEATED_ELEMENT = 2
    USER_NOT_FOUND = 3

class PostgresDatabase:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD")
        )
    
    def register_user(self, user: models.user.NewUser):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL AddUser(%s, %s, %s, %s)",
                (user.name, user.mail, user.password, user.role)
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
    
    def delete_user(self, user: models.user.DelUser):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL DeleteUser(%s)", (user.mail,)
            )
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION
    
    def edit_user(self, user: models.user.EditUser):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "CALL EditUser(%s, %s, %s, %s, %s)",
                (user.mail, user.name, user.newMail, user.password, user.role)
            )
            self.connection.commit()
            cursor.close()
            return ResultCode.SUCCESS
        except psycopg2.errors.InFailedSqlTransaction:
            self.connection.rollback()
            return ResultCode.FAILED_TRANSACTION

class MongoDatabase:
    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")

class RedisDatabase:
    def __init__(self):
        self.connection = redis.Redis(
            host="redis",
            port=6379,
            db=0,
            decode_responses=True
        )
        self.connection.ping()
    
    def set_hash_data(self, key, value):
        self.connection.hset(key, mapping=dict(value))
        self.connection.expire(key, 100)
        return ResultCode.SUCCESS
    
    def delete_hash_data(self, key, llaves):
        self.connection.hdel(key, *llaves)
        return ResultCode.SUCCESS
