from typing import ClassVar, Generic, TypeVar
from pydantic import BaseModel

EventPayload = TypeVar("EventPayload")

class DomainEvent(BaseModel, Generic[EventPayload]):
    name : ClassVar[str] = "event_name"
    payload : EventPayload