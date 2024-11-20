#!/usr/bin/env python3
"""User model for SQLAlchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User class that represents a database table named users
    Attributes:
        id (int): The integer primary key
        email (str): The non-nullable email string
        hashed_password (str): The non-nullable password string
        session_id (str): The nullable session ID string
        reset_token (str): The nullable reset token string
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
