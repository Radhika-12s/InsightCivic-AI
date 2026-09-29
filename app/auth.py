import hashlib
import os


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):
    try:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return password_hash == stored_hash

    except (ValueError, TypeError):
        return False


def register_user(username, email, password):
    from database import create_user

    password_hash = hash_password(password)

    return create_user(
        username=username,
        email=email,
        password_hash=password_hash,
        role="user"
    )


def authenticate_user(username, password):
    from database import get_user_by_username

    user = get_user_by_username(username)

    if user is None:
        return None

    if verify_password(password, user["password_hash"]):
        return user

    return None