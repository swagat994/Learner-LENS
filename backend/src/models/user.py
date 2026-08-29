from datetime import datetime
from typing import Any

from bson import ObjectId


class User:
    def __init__(
        self,
        name: str,
        email: str,
        hashed_password: str,
    ):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": str(data["_id"]),
            "name": data["name"],
            "email": data["email"],
        }