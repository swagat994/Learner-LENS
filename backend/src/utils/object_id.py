from bson import ObjectId

from src.exceptions.custom import InvalidObjectIdError


def validate_object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise InvalidObjectIdError()

    return ObjectId(value)