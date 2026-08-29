from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt.exceptions import PyJWTError

from src.auth.jwt import decode_access_token
from src.exceptions.custom import (
    InvalidTokenError,
    UserNotFoundError,
)
from src.repositories.user import UserRepository


security = HTTPBearer()

user_repository = UserRepository()


async def get_current_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        return decode_access_token(
            credentials.credentials
        )

    except PyJWTError:
        raise InvalidTokenError()


async def get_current_user(
    payload=Depends(get_current_payload),
):
    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    user = await user_repository.get_user_by_id(
        user_id
    )

    if user is None:
        raise UserNotFoundError()

    user["id"] = str(user["_id"])
    del user["_id"]

    return user