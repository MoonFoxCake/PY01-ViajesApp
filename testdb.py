# test_db.py
import pytest
from unittest.mock import patch, MagicMock
from db import Database, ResultCode
import os
import psycopg2
from enum import Enum
from passlib.context import CryptContext

@pytest.fixture
def mock_db():
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def db(mock_db):
    return Database()

def test_register_user_success(db, mock_db):
    mock_cursor = mock_db.cursor.return_value
    db.connection.commit.return_value = None
    result = db.register_user(MagicMock(name="test", mail="test@mail.com", password="password", role="user"))
    assert result == ResultCode.SUCCESS

def test_register_user_failed_transaction(db, mock_db):
    mock_db.cursor.side_effect = psycopg2.errors.InFailedSqlTransaction
    result = db.register_user(MagicMock(name="test", mail="test@mail.com", password="password", role="user"))
    assert result == ResultCode.FAILED_TRANSACTION

def test_register_user_repeated_element(db, mock_db):
    mock_db.cursor.side_effect = psycopg2.errors.UniqueViolation
    result = db.register_user(MagicMock(name="test", mail="test@mail.com", password="password", role="user"))
    assert result == ResultCode.REPEATED_ELEMENT

# Similarly, write tests for delete_user, edit_user, create_post, authenticate_user, and get_user_info

def test_authenticate_user_success(db, mock_db):
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = ["hashed_password"]
    db.pwd_context.verify = MagicMock(return_value=True)
    result = db.authenticate_user("test@mail.com", "password")
    assert result == ResultCode.SUCCESS

def test_authenticate_user_not_found(db, mock_db):
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = None
    result = db.authenticate_user("test@mail.com", "password")
    assert result == ResultCode.USER_NOT_FOUND

def test_authenticate_user_invalid_password(db, mock_db):
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchone.return_value = ["hashed_password"]
    db.pwd_context.verify = MagicMock(return_value=False)
    result = db.authenticate_user("test@mail.com", "password")
    assert result == ResultCode.INVALID_PASSWORD

# Add more tests for other methods...
