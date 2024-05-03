import base64
import json
import re
import uuid
from typing import Annotated, Type, Any

from pydantic import Field, BaseModel, GetCoreSchemaHandler, field_validator
from pydantic_core import core_schema


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


def entity_json_encoder(obj):
    if isinstance(obj, GenericUUID):
        return str(obj)
    return json.json_encoder(obj)

class ValueObject(BaseModel):
    pass


Email = Annotated[str, Field(min_length=5, max_length=200, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')]
LinkToImage = Annotated[str, Field(min_length=1, pattern=r'^.*\.(png|jpe?g|gif)$')]


class Base64Field(BaseModel):
    image: str

    @field_validator('image')
    def validate_base64(cls, v):
        try:
            base64.b64decode(v, validate=True)
        except Exception:
            raise ValueError('Invalid base64 format')
        return v
