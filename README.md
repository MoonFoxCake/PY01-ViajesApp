# API Endpoints Guide

## User Endpoints (PostgreSQL)

### Register User
- **Method**: POST
- **URL**: `http://localhost:8000/registerUser`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "Name": "John Doe",
        "Mail": "john.doe@example.com",
        "Password": "password123",
        "Role": 1
    }
    ```

### Delete User
- **Method**: POST
- **URL**: `http://localhost:8000/deleteUser`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "UserID": 1
    }
    ```

### Edit User
- **Method**: POST
- **URL**: `http://localhost:8000/editUser`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "UserID": 1,
        "Name": "John Doe Updated",
        "Mail": "john.doe.updated@example.com",
        "Password": "newpassword123",
        "Role": 1
    }
    ```

### Login
- **Method**: POST
- **URL**: `http://localhost:8000/login`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "Mail": "john.doe@example.com",
        "Password": "password123"
    }
    ```

## Post Endpoints (MongoDB)

### Create Post
- **Method**: POST
- **URL**: `http://localhost:8000/createPost`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "AuthorID": 1,
        "Texto": "This is a new post",
        "MediaType": "text",
        "MediaURL": "",
        "Caption": "",
        "Likes": [],
        "Comentarios": []
    }
    ```

### Get Post
- **Method**: GET
- **URL**: `http://localhost:8000/post/{post_id}`
- **Headers**: None
- **Body**: None

### Like Post
- **Method**: POST
- **URL**: `http://localhost:8000/likePost`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "PostID": "60d5ec49f8d2f8b4b8f8b8f8",
        "UserID": 1
    }
    ```

### Comment Post
- **Method**: POST
- **URL**: `http://localhost:8000/commentPost`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "PostID": "60d5ec49f8d2f8b4b8f8b8f8",
        "UserID": 1,
        "Texto": "This is a comment",
        "Likes": []
    }
    ```

## Destination Endpoints (MongoDB)

### Create Destination
- **Method**: POST
- **URL**: `http://localhost:8000/createDestino`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "Pais": "Estados Unidos",
        "Destino": "Hawaii",
        "Link al destino": "https://www.gohawaii.com/islands/oahu/regions/honolulu",
        "Descripcion": "Sitio turistico en estados unidos ideal para unas vacaciones tropicales",
        "Likes": [],
        "Comentarios": [],
        "Rating": 9.3
    }
    ```

### Comment Destination
- **Method**: POST
- **URL**: `http://localhost:8000/commentDestino`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "DestinoID": "60d5ec49f8d2f8b4b8f8b8f8",
        "UserID": 1,
        "Texto": "This is a comment",
        "Likes": []
    }
    ```

### Like Destination
- **Method**: POST
- **URL**: `http://localhost:8000/likeDestino`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "DestinoID": "60d5ec49f8d2f8b4b8f8b8f8",
        "UserID": 1
    }
    ```

## Comment Endpoints (MongoDB)

### Like Comment
- **Method**: POST
- **URL**: `http://localhost:8000/likeComment`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "PostID": "60d5ec49f8d2f8b4b8f8b8f8",
        "CommentID": "60d5ec49f8d2f8b4b8f8b8f9",
        "UserID": 1
    }
    ```

## Bucket List Endpoints (MongoDB)

### Create Bucket List
- **Method**: POST
- **URL**: `http://localhost:8000/createBucketList`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "UserID": 1,
        "Nombre": "My Bucket List",
        "Destinos": ["60d5ec49f8d2f8b4b8f8b8f8"]
    }
    ```

### Follow Bucket List
- **Method**: POST
- **URL**: `http://localhost:8000/followBucketList`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "UserID": 1,
        "BucketListID": "60d5ec49f8d2f8b4b8f8b8f8"
    }
    ```

## Trip Endpoints (MongoDB)

### Create Trip
- **Method**: POST
- **URL**: `http://localhost:8000/createTrip`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "UserID": 1,
        "DestinoID": "60d5ec49f8d2f8b4b8f8b8f8",
        "FechaInicio": "2023-01-01",
        "FechaFin": "2023-01-10",
        "Descripcion": "Trip to Hawaii"
    }
    ```

