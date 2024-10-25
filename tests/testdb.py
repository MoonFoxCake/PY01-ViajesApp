import pytest
from app import *
import models
import models.Trips
import models.posts
from bson.objectid import ObjectId
from fastapi import Response

pytest.objectId = None

@pytest.mark.asyncio
async def test_create_post():
    testPost = models.posts.NewPost(
        AuthorID=1,
        Texto="Post de prueba.",
        MediaType="text"
    )
    res = await create_post(testPost)
    pytest.objectId = res["id"]
    assert res["message"] == "Post created successfully"

@pytest.mark.asyncio
async def test_get_version():
    res = await get_version()
    assert res == {"message": "Connection acknowledge"}

@pytest.mark.asyncio
async def test_register_user():
    testUser = models.user.NewUser(
        name="test",
        mail="test@prueba.com",
        password="testPassword",
        role=1
    )
    res = await register_user(testUser)
    assert res == {"message": "User registered successfully"}

@pytest.mark.asyncio
async def test_register_user_conflict():
    testUser = models.user.NewUser(
        name="test",
        mail="test@prueba.com",
        password="testPassword",
        role=1
    )
    res = await register_user(testUser)
    assert res.status_code == status.HTTP_409_CONFLICT

@pytest.mark.asyncio
async def test_edit_user():
    testUser = models.user.EditUser(
        mail="test@prueba.com",
        name="test2"
    )
    res = await edit_user(testUser)
    assert res == {"message": "User edited successfully"}

@pytest.mark.asyncio
async def test_edit_user_notfound():
    testUser = models.user.EditUser(
        mail="esteNoDeberiaExistir@prueba.com",
        name="test2"
    )
    res = await edit_user(testUser)
    assert res.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_login_user():
    testUser = models.user.NewUser(
        name="test",
        mail="test@prueba.com",
        password="testPassword",
        role=1
    )
    res = await login(testUser)
    assert res == {"message": "Sesión refrescada. Login se hizo exitosamente."}

@pytest.mark.asyncio
async def test_login_user_pwd_incorrect():
    testUser = models.user.NewUser(
        name="test",
        mail="test@prueba.com",
        password="incorrectPwd",
        role=1
    )
    res = await login(testUser)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_login_user_notfound():
    testUser = models.user.NewUser(
        name="test",
        mail="esteNoDeberiaExistir@prueba.com",
        password="testPassword",
        role=1
    )
    res = await login(testUser)
    assert res.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_fetch_post():
    res = await get_post(str(pytest.objectId))
    assert res == {
        "AuthorID":1, 
        "Texto":"Post de prueba.", 
        "MediaType":"text",
        "MediaURL":"",
        "Caption":"",
        "Likes":[],
        "Comentarios":[]
    }

@pytest.mark.asyncio
async def test_like_post():
    testPost = models.posts.LikePost(
        PostID=str(pytest.objectId),
        LikeAuthorID="1"
    )
    res = await like_post(testPost)
    assert res == {"message": "Post liked successfully"}

@pytest.mark.asyncio
async def test_comment_post():
    testComment = models.posts.PostComment(
        PostID=str(pytest.objectId),
        UserID="1",
        Texto="Prueba fea."
    )
    res = await add_comment(testComment)
    assert res["message"] == "Comment added successfully and stored temporarily in Redis"

@pytest.mark.asyncio
async def test_create_destino():
    testDestination = models.Trips.NewDestination(
        AuthorID="1",
        DestinationName="TEC",
        Description="Universidad",
        Location="Cartago"
    )
    res = await create_destino(testDestination)
    assert res == {"message": "Destination created successfully"}

@pytest.mark.asyncio
async def test_comment_destination():
    testComment = models.posts.Comment(
        UserID="1",
        Texto="Prueba fea."
    )
    res = await add_comment_destino(1, testComment)
    assert res == {"message": "Comment added successfully"}

@pytest.mark.asyncio
async def test_like_destination():
    testComment = models.Trips.LikeDestination(
        PostID="1"
    )
    res = await like_destino(testComment)
    assert res == {"message": "Post liked successfully"}

@pytest.mark.asyncio
async def test_create_bucket_list():
    testComment = models.Trips.BucketListCreation(
       AuthorID="1",
       Destinos=["1"]
    )
    res = await create_bucket_list(testComment)
    assert res == {"message": "Bucket list created successfully"}

@pytest.mark.asyncio
async def test_create_trip():
    testComment = models.Trips.CreateTrip(
       Participants=["1"],
       Destinos=["1"]
    )
    res = await create_trip(testComment)
    assert res == {"message": "Trip created successfully"}

@pytest.mark.asyncio
async def test_delete_user():
    testUser = models.user.DelUser(mail="test@prueba.com")
    res = await delete_user(testUser)
    assert res == {"message": "User deleted successfully"}

@pytest.mark.asyncio
async def test_delete_user_notfound():
    testUser = models.user.DelUser(mail="esteNoDeberiaExistir@prueba.com")
    res = await delete_user(testUser)
    assert res.status_code == status.HTTP_404_NOT_FOUND