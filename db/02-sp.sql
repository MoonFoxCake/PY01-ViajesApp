\c userssm

CREATE OR REPLACE PROCEDURE AddRole(Permiso VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Roles (Permiso)
    VALUES (Permiso);
END;
$$;

CREATE OR REPLACE PROCEDURE AddUser(
    Name VARCHAR,
    Mail VARCHAR,
    Password VARCHAR,
    Role INT DEFAULT 1
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Users (Name, Mail, Password, Role)
    VALUES (Name, Mail, Password, Role);
END;
$$;

CREATE OR REPLACE PROCEDURE EditUser(
    p_Mail VARCHAR,
    p_Name VARCHAR,
    p_NewMail VARCHAR,
    p_Password VARCHAR,
    p_Role INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    oldMail VARCHAR;
BEGIN

    SELECT Mail INTO oldMail
    FROM Users
    WHERE Mail = p_Mail;

    UPDATE Users
    SET Name = COALESCE(p_Name, Users.Name),
        Mail = COALESCE(p_NewMail, Users.Mail),
        Password = COALESCE(p_Password, Users.Password),
        Role = COALESCE(p_Role, Users.Role)
    WHERE UserID = oldMail;
END;
$$;

CREATE OR REPLACE PROCEDURE DeleteUser(inUserMail VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Users WHERE mail = inUserMail;
END;
$$;

CREATE OR REPLACE PROCEDURE CreatePost(AuthorID INT, Texto TEXT, MediaType VARCHAR, MediaURL VARCHAR, Caption VARCHAR DEFAULT NULL)
LANGUAGE plpgsql
AS $$
DECLARE
    NewPostID INT;
BEGIN
    -- Insert into Posts table
    INSERT INTO Posts (AuthorID)
    VALUES (AuthorID)
    RETURNING PostID INTO NewPostID;

    -- Insert into PostDetails table
    INSERT INTO PostDetails (PostID, Texto)
    VALUES (NewPostID, Texto);

    -- Insert into Media table if MediaURL is provided
    IF MediaURL IS NOT NULL THEN
        INSERT INTO Media (PostID, MediaType, MediaURL, Caption)
        VALUES (NewPostID, MediaType, MediaURL, Caption);
    END IF;
END;
$$;

--CREATE OR REPLACE PROCEDURE ValidateUser(
--    IN input_username VARCHAR,
--    IN input_password VARCHAR,
--    OUT is_valid BOOLEAN
--)
--LANGUAGE plpgsql
--AS $$
--BEGIN
    -- Initialize the result to false
--    is_valid := FALSE;

    -- Check if there is a matching user
--    IF EXISTS (
--        SELECT 1
--        FROM Users
--        WHERE Name = input_username AND Password = input_password
--    ) THEN
--       is_valid := TRUE;
--    END IF;
--END;
--$$;

--test un insert de usuario

--http://localhost:8000/register

--en postman, opcion body, y luego raw

--{
--    "name": "Task 1",
--    "mail": "Do something",
--    "password": "your_password_here",
--    "role": 1
--}


Call AddRole('Usuario');

Call AddRole('Admin');


--CALL ValidateUser('Test', 'Test', @result);