-- creates database For postgres
CREATE DATABASE UsersSM;

\c UsersSM


CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Mail VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role INT REFERENCES Roles(RolID) NOT NULL
);

