import abc
from typing import Generic, TypeVar

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID

EntityType = TypeVar("EntityType", bound=Entity)
EntityId = TypeVar("EntityId", bound=GenericUUID)


class GenericRepository(Generic[EntityId, EntityType], metaclass=abc.ABCMeta):
    """An interface for a generic repository"""

    @abc.abstractmethod
    def add(self, entity: EntityType):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, id: EntityId):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: EntityId) -> EntityType:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, entity: EntityType):
        raise NotImplementedError()