import uuid
import time

import flask_bcrypt
from flask import request
from app import get_app
from errors import ApiError
from config import TOKEN_TTL
from models import Token

app = get_app()
bcrypt = flask_bcrypt.Bcrypt(app)


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password.encode()).decode()


def check_password(
        password_hash: str,
        password: str,
) -> bool:
    return bcrypt.check_password_hash(password_hash.encode(), password.encode())


def check_auth(session) -> Token:
    try:
        token = uuid.UUID(request.headers.get("token"))
    except (ValueError, TypeError):
        raise ApiError(403, "incorrect token")
    token = session.query(Token).get(token)

    if token is None:
        raise ApiError(403, "incorrect token")

    if time.time() - token.created_at.timestamp() > TOKEN_TTL:
        raise ApiError(403, "incorrect token")

    return token
