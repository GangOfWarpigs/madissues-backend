import abc
from typing import Generic, TypeVar

from madissues_backend.core.shared.domain import entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Entity = TypeVar("Entity", bound=entity.Entity)
EntityId = TypeVar("EntityId", bound=GenericUUID)


class GenericRepository(Generic[EntityId, Entity], metaclass=abc.ABCMeta):
    """An interface for a generic repository"""

    @abc.abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: EntityId) -> Entity:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, entity: Entity):
        raise NotImplementedError()