from src.exceptions.custom import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from src.auth.jwt import create_access_token
from src.auth.security import (
    hash_password,
    verify_password,
)


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_user(
        self,
        user: UserCreate,
    ) -> UserResponse:

        existing_user = await self.repository.get_user_by_email(
            user.email
        )

        if existing_user:
            raise UserAlreadyExistsError(user.email)

        hashed_password = hash_password(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
        )

        created_user = await self.repository.create_user(
            new_user
        )

        return UserResponse(
            id=str(created_user["_id"]),
            name=created_user["name"],
            email=created_user["email"],
        )

    async def login_user(
        self,
        credentials: UserLogin,
    ) -> TokenResponse:

        user = await self.repository.get_user_by_email(
            credentials.email
        )

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(
            credentials.password,
            user["hashed_password"],
        ):
            raise InvalidCredentialsError()

        token = create_access_token(
            str(user["_id"])
        )

        return TokenResponse(
            access_token=token,
        )