import abc
from typing import Dict
from typing import Generic

from madissues_backend.core.shared.domain.entity import EntityId, EntityType


class EntityTable:
    def __init__(self):
        self.tables: Dict[str, Dict[EntityId, EntityType]] = {
            'owners': {},
            'organizations': {},
            'students': {},
            'issues': {}
        }



class GenericMockRepository(Generic[EntityId, EntityType], metaclass=abc.ABCMeta):
    """An interface for a generic mock repository"""

    def __init__(self, entity_table: EntityTable):
        self.entity_table = entity_table
