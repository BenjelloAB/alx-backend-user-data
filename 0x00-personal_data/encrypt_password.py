#!/usr/bi/env python3
"""
Encrypting passwords file..
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """method to hash the password"""
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """A method to validate password with the hashed password"""
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
