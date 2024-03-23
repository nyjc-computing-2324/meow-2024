import os
import hashlib

def create_hash(password: str) -> tuple[str, bytes]:
    """
    Takes in the password the user provides as a string
    Returns the hash of the password as a string of hex characters
    Also returns the salt as bytes
    Hash and salt to be stored in database

    Example:
    >>> hash, salt = create_hash("thisismypassword")
    >>> print(hash)
    61f3b39102f140aabcc2af927d33066adc565d35d77529c550cfb3f8a2708da1
    >>> print(salt)
    b'\xdf\x93\xa2\xa4\xf6\xbb9\x83\x97*\xcbj\xf4=\xca\xaf[\x1d@/\xbc\xac\xf9\x01\n\x119\xc0M\xdf\xd4\x94'
    """
    salt = os.urandom(32)
    salted_pass = bytes(password,"UTF-8") + salt
    hashed_pass = hashlib.sha256(salted_pass).hexdigest()
    return hashed_pass, salt

def check_password(password: str, password_hash: str, salt: bytes) -> bool:
    """
    Takes in the password the user provides as a string
    Takes in the password_hash stored in the database
    Takes in the salt stored in the database
    Returns boolean: True if password is correct

    Example:
    >>> check_password("thisismypassword", "61f3b39102f140aabcc2af927d33066adc565d35d77529c550cfb3f8a2708da1", b'\xdf\x93\xa2\xa4\xf6\xbb9\x83\x97*\xcbj\xf4=\xca\xaf[\x1d@/\xbc\xac\xf9\x01\n\x119\xc0M\xdf\xd4\x94')
    True
    >>> check_password("thisisnotmypassword", "61f3b39102f140aabcc2af927d33066adc565d35d77529c550cfb3f8a2708da1", b'\xdf\x93\xa2\xa4\xf6\xbb9\x83\x97*\xcbj\xf4=\xca\xaf[\x1d@/\xbc\xac\xf9\x01\n\x119\xc0M\xdf\xd4\x94')
    False
    """
    salted_pass = bytes(password,"UTF-8") + salt
    hashed_pass = hashlib.sha256(salted_pass).hexdigest()
    return hashed_pass == password_hash
