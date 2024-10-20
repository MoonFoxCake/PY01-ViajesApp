import os
import psycopg2
import pymongo
import pymongo.collection
import pymongo.results
import redis
import models.Trips
import models.user
import models.posts
from enum import Enum

class ResultCode(Enum):
    SUCCESS = 0
    FAILED_TRANSACTION = 1
    REPEATED_ELEMENT = 2
    USER_NOT_FOUND = 3
    POST_NOT_FOUND = 4
 
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
        self.connection = pymongo.MongoClient("mongodb://root:root@dbmongo:27017/")
        self.db = self.connection["ViajesDB"]
        self.posts = self.db["posts"]
        self.destinos = self.db["destinos"]
        self.bucketLists = self.db["bucketLists"]
        self.trips = self.db["trips"]
    
    def create_post(self, post: models.posts.NewPost):
        result: pymongo.results.InsertOneResult = self.posts.insert_one( dict(post) )
        if result.acknowledged:
            return [ResultCode.SUCCESS, result.inserted_id]
        return ResultCode.FAILED_TRANSACTION
    
    def get_post(self, post: models.posts.GetPost):
        return self.posts.find_one({"_id": post.PostID}) | ResultCode.POST_NOT_FOUND
        
    def like_post(self, post: models.posts.LikePost):
        result: pymongo.results.UpdateResult = self.posts.update_one(
            {"_id": post.PostID},
            {"$inc": {"Likes": 1} }
        )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION

    def add_comment_post(self, postID: str, comment: models.posts.Comment):
        result = self.posts.update_one(
            {"_id": postID},
            {"$push": {"Comentarios": dict(comment)} }
        )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION

    def create_destino(self, destino: models.Trips.NewDestination):
        result: pymongo.results.InsertOneResult = self.destinos.insert_one( dict(destino) )
        if result.acknowledged:
            return [ResultCode.SUCCESS, result.inserted_id]
        return ResultCode.FAILED_TRANSACTION

    def add_comment_destino(self, destinoID: str, comment: models.Trips.Comment):
        result = self.posts.update_one(
            {"_id": destinoID},
            {"$push": {"Comentarios": dict(comment)} }
        )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION
    
    def add_like_destino(self, post: models.Trips.LikeDestination):
        result: pymongo.results.UpdateResult = self.posts.update_one(
            {"_id": post.PostID},
            {"$inc": {"Likes": 1} }
        )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION

    def create_bucket_list(self, bucketList: models.Trips.BucketListCreation):
        result: pymongo.results.InsertOneResult = self.bucketLists.insert_one( dict(bucketList) )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION

    #! Falta lo de hacer que se puedan seguir bucket lists.

    def create_trip(self, trip: models.Trips.CreateTrip):
        result: pymongo.results.InsertOneResult = self.trips.insert_one( dict(trip) )
        if result.acknowledged:
            return ResultCode.SUCCESS
        return ResultCode.FAILED_TRANSACTION

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
