import json
from dataclasses import field
from typing import Generic, TypeVar
from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from .value_objects import GenericUUID, entity_json_encoder

EntityId = TypeVar("EntityId", bound=GenericUUID)


class Entity(BaseModel, Generic[EntityId]):
    id: EntityId

    json_encoder = entity_json_encoder

    def validate_field(self, name, value):
        self.__class__.__pydantic_validator__.validate_assignment(self.__class__.model_construct(), name, value)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        for field_name, field_value in d.items():
            if isinstance(field_value, GenericUUID):
                d[field_name] = str(field_value)
        return d

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
