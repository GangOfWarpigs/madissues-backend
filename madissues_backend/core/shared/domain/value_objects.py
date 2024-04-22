import uuid
from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass


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


class Email(str):
    def __new__(cls, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return super().__new__(cls, email)