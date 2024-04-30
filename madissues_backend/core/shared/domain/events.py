from typing import ClassVar, Generic, TypeVar
from pydantic import BaseModel, Field

EventPayload = TypeVar("EventPayload")


class DomainEvent(BaseModel, Generic[EventPayload]):
    name: str = Field(init=False)
    payload: EventPayload
