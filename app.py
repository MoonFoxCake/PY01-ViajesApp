from fastapi import FastAPI, status, Response
from db import PostgresDatabase, MongoDatabase, RedisDatabase, ResultCode
from models.posts import Comment, NewPost, LikePost
from models.PostsMongo import NewPost
from models.Trips import NewDestination, LikeDestination, BucketListCreation, CreateTrip
from models.user import NewUser, DelUser, EditUser
from fastapi import FastAPI, Response, status
from db import PostgresDatabase, MongoDatabase, ResultCode
import uvicorn

app: FastAPI = FastAPI()
postgresDB: PostgresDatabase = PostgresDatabase()
mongoDB: MongoDatabase = MongoDatabase()
redisDB: RedisDatabase = RedisDatabase()

@app.get("/")
async def get_version():
    return {"message": "Connection acknowledge"}

# -----------------------------------------------------------
# Endpoints de usuarios (PostgreSQL) 

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
    
#Cambios Felipe
@app.post("/login")
async def login(user: NewUser, response: Response):
    # Primero verifica si el usuario existe en PostgreSQL
    result = postgresDB.authenticate_user(user.mail, user.password)
    
    if result == ResultCode.SUCCESS:
        # Intenta obtener la sesión del usuario en Redis
        session = redisDB.get_user_session(user.mail)

        if session:
            # Refresca la expiración si la sesión existe
            redisDB.refresh_user_session(user.mail)
            return {"message": "Sesión refrescada. Login se hizo exitosamente."}
        else:
            # Si no existe, crea una nueva sesión en Redis
            redisDB.set_user_session(user.mail, {"name": user.name, "mail": user.mail, "role": user.role})
            return {"message": "Login exitoso, se creó una nueva sesión."}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    elif result == ResultCode.INVALID_PASSWORD:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid password")
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Login failed")

#Cambios Felipe

# -----------------------------------------------------------
# Endpoints de MongoDB    

@app.post("/createPost")
async def create_post(post: NewPost):
    result = mongoDB.create_post(post)
    objID = str(result[1])
    if result[0] == ResultCode.SUCCESS:
        redisDB.set_hash_data(objID, post)
        return {"message": "Post created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.get("/post/{post_id}")
async def get_post(post_id: str):
    result = mongoDB.get_post(post_id)
    if result:
        return result
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/likePost")
async def like_post(post: LikePost):
    result = mongoDB.like_post(post)
    if result == ResultCode.SUCCESS:
        return {"message": "Post liked successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/commentPost")
async def add_comment(post_id: str, comment: Comment):
    result = mongoDB.add_comment_post(post_id, comment)
    if result == ResultCode.SUCCESS:
        return {"message": "Comment added successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/createDestino")
async def create_destino(destination: NewDestination):
    result = mongoDB.create_destino(destination)
    if result[0] == ResultCode.SUCCESS:
        redisDB.set_hash_data(str(result[1]), destination)
        return {"message": "Destination created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/commentDestino")
async def add_comment_destino(destino_id: str, comment: Comment):
    result = mongoDB.add_comment_destino(destino_id, comment)
    if result == ResultCode.SUCCESS:
        return {"message": "Comment added successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/likeDestino")
async def like_destino(destination: LikeDestination):
    result = mongoDB.add_like_destino(destination)
    if result == ResultCode.SUCCESS:
        return {"message": "Post liked successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/createBucketList")
async def create_bucket_list(bucket_list: BucketListCreation):
    result = mongoDB.create_bucket_list(bucket_list)
    if result == ResultCode.SUCCESS:
        return {"message": "Bucket list created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@app.post("/createTrip")
async def create_trip(trip: CreateTrip):
    result = mongoDB.create_trip(trip)
    if result == ResultCode.SUCCESS:
        return {"message": "Trip created successfully"}
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#Cambios Felipe
@app.post("/followBucketList/{bucketlist_id}")
async def follow_bucket_list(bucketlist_id: str, user: dict):
    user_id = user['user_id']
    result = mongoDB.seguir_bucket_list(user_id, bucketlist_id)
    if result == ResultCode.SUCCESS:
        return {"message": "User is now following the Bucket List successfully"}
    elif result == ResultCode.USER_NOT_FOUND:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Failed to follow the Bucket List")
#Cambios Felipe

# -----------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
