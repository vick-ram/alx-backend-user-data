#!/usr/bin/env python3
"""encrypt_password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt, returns the
    hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
