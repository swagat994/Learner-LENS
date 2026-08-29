class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class UserAlreadyExistsError(AppException):

    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists.",
            status_code=409,
            error_code="USER_ALREADY_EXISTS",
        )


class InvalidCredentialsError(AppException):

    def __init__(self):
        super().__init__(
            message="Invalid email or password.",
            status_code=401,
            error_code="INVALID_CREDENTIALS",
        )


class InvalidTokenError(AppException):

    def __init__(self):
        super().__init__(
            message="Invalid or expired access token.",
            status_code=401,
            error_code="INVALID_TOKEN",
        )


class UserNotFoundError(AppException):

    def __init__(self):
        super().__init__(
            message="User not found.",
            status_code=404,
            error_code="USER_NOT_FOUND",
        )


class InvalidObjectIdError(AppException):

    def __init__(self):
        super().__init__(
            message="Invalid resource ID.",
            status_code=400,
            error_code="INVALID_OBJECT_ID",
        )