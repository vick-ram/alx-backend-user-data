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
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __str__(self) -> str:
        return self.email
