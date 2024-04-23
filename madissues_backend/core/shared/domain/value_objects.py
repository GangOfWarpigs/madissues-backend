import uuid
from typing import Annotated

from pydantic import AfterValidator, BaseModel


class GenericUUID(uuid.UUID):
    @classmethod
    def next_id(cls):
        return GenericUUID(int=uuid.uuid4().int)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, validation_info):
        if isinstance(value, str):
            return cls(value)
        if not isinstance(value, uuid.UUID):
            raise ValueError('Invalid UUID')
        return cls(value.hex)


def email_is_valid(email: str) -> str:
    assert "@" in email
    return email


Email = Annotated[str, AfterValidator(email_is_valid)]


class ValueObject(BaseModel):
    pass
