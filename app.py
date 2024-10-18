from fastapi import FastAPI, status, Response
from db import PostgresDatabase, MongoDatabase, RedisDatabase, ResultCode
from models.NewPost import Comment, NewPost
from models.PostsMongo import NewPost
from models.user import NewUser, DelUser, EditUser
import uvicorn

app: FastAPI = FastAPI()
postgresDB: PostgresDatabase = PostgresDatabase()
mongoDB: MongoDatabase = MongoDatabase()
redisDB: RedisDatabase = RedisDatabase()

@app.get("/")
async def get_version():
    return {"message": "Connection acknowledge"}

@app.post("/registerUser")
async def register_user(user: NewUser):
    result = postgresDB.register_user(user)
    if result == ResultCode.SUCCESS:
        redisDB.set_hash_data(user.mail, user)
        return {"message": "User registered successfully"}
    elif result == ResultCode.REPEATED_ELEMENT:
        return Response(status_code=status.HTTP_409_CONFLICT)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/deleteUser")
async def delete_user(user: DelUser):
    result = postgresDB.delete_user(user)
    if result == ResultCode.SUCCESS:
        redisDB.delete_hash_data(user.mail, ["name", "mail", "password", "role"])
        return {"message": "User deleted successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/editUser")
async def edit_user(user: EditUser):
    result = postgresDB.edit_user(user)
    if result == ResultCode.SUCCESS:
        return {"message": "User edited successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/posts")
async def create_post(post: NewPost):
    result = mongoDB.create_post(post)
    if result == ResultCode.SUCCESS:
        return {"message": "Post created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/posts/{post_id}")
async def get_post(post_id: str):
    result = mongoDB.get_post(post_id)
    if result:
        return result
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/posts/{post_id}/like")
async def like_post(post_id: str):
    result = mongoDB.like_post(post_id)
    if result == ResultCode.SUCCESS:
        return {"message": "Post liked successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/posts/{post_id}/comment")
async def add_comment(post_id: str, comment: Comment):
    result = mongoDB.add_comment(post_id, comment)
    if result == ResultCode.SUCCESS:
        return {"message": "Comment added successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
