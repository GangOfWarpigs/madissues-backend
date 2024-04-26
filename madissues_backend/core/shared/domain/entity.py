from dataclasses import field
from typing import Generic, TypeVar
from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from .value_objects import GenericUUID

EntityId = TypeVar("EntityId", bound=GenericUUID)


class Entity(BaseModel, Generic[EntityId]):
    id: EntityId


EntityType = TypeVar("EntityType", bound=Entity)


class AggregateRoot(Entity[EntityId]):
    """Consists of 1+ entities. Spans transaction boundaries."""
    events: list = field(default_factory=list)

    def register_event(self, event: DomainEvent):
        self.events.append(event)

    def collect_events(self):
        events = self.events
        self.events = []
        return events
