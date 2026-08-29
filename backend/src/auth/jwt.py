from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError

from src.config.settings import settings


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt.secret_key,
        algorithms=[settings.jwt.algorithm],
    )