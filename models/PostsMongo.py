#from pydantic import BaseModel, Field
#from typing import Optional, List
from pymongo import MongoClient
from models.posts import NewPost  # NewPost desde el archivo de modelos
#from models.Comment import Comment  #  Comment
from bson.objectid import ObjectId
from db import ResultCode

#class Comment(BaseModel):
 #   UserID: str
  #  Texto: str

#class NewPost(BaseModel):
 #   AuthorID: str
  #  Texto: Optional[str] = None
   # MediaURL: Optional[str] = None
    #Likes: List[str] = []
    #Comentarios: List[Comment] = []

class MongoDatabase:
    def __init__(self):
        # Conexión a MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['ViajesDB']
        self.posts = self.db['posts']  # Colección de posts

    def create_post(self, post: NewPost):
        try:
            # Convierte el modelo NewPost a un diccionario y lo inserta en MongoDB
            post_data = post.dict()
            result = self.posts.insert_one(post_data)
            if result.inserted_id:
                return ResultCode.SUCCESS
            else:
                return ResultCode.FAILED_TRANSACTION
        except Exception as e:
            print(f"Error creating post: {e}")
            return ResultCode.FAILED_TRANSACTION

    def get_post(self, post_id: str):
        try:
            # Busca el post en MongoDB por ID
            post = self.posts.find_one({"_id": ObjectId(post_id)})
            if post:
                return post
            else:
                return None
        except Exception as e:
            print(f"Error retrieving post: {e}")
            return None

    def like_post(self, post_id: str):
        try:
            # Incrementa los likes de un post en MongoDB
            result = self.posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$inc": {"Likes": 1}}
            )
            if result.modified_count > 0:
                return ResultCode.SUCCESS
            else:
                return ResultCode.FAILED_TRANSACTION
        except Exception as e:
            print(f"Error liking post: {e}")
            return ResultCode.FAILED_TRANSACTION

#    def add_comment(self, post_id: str, comment: Comment):
#        try:
#            # Añade un comentario a un post en MongoDB
#            result = self.posts.update_one(
#                {"_id": ObjectId(post_id)},
#                {"$push": {"Comentarios": comment.dict()}}
#            )
#            if result.modified_count > 0:
#                return ResultCode.SUCCESS
#            else:
#                return ResultCode.FAILED_TRANSACTION
#        except Exception as e:
#            print(f"Error adding comment: {e}")
#            return ResultCode.FAILED_TRANSACTION