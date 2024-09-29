-- creates database For postgres
CREATE DATABASE tasks;

\c tasks


CREATE TABLE Roles (
    RolID SERIAL PRIMARY KEY,
    Permiso VARCHAR(255) NOT NULL
);

CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Mail VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role INT REFERENCES Roles(RolID) NOT NULL
);

CREATE TABLE Posts (
    PostID SERIAL PRIMARY KEY,
    AuthorID INT REFERENCES Users(UserID) NOT NULL
);

CREATE TABLE PostDetails (
    PostDetailID SERIAL PRIMARY KEY,
    PostID INT REFERENCES Posts(PostID) NOT NULL,
    Texto TEXT
);

CREATE TABLE Media (
    MediaID SERIAL PRIMARY KEY,
    PostID INT REFERENCES Posts(PostID) NOT NULL,
    MediaType VARCHAR(15) NOT NULL,  -- 'image' or 'video'
    MediaURL VARCHAR(255) NOT NULL,
    Caption VARCHAR(255)
);
