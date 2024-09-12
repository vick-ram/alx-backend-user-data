#!/usr/bin/env python3
"""
User model definition module.
Defines a SQLAlchemy model for a users table with the following attributes:
id, email, hashed_password, session_id, reset_token.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """User class mapped to the users table."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __str__(self) -> str:
        return self.email
