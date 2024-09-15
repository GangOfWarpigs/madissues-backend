import abc
import json
import os
import pickle
from typing import Dict
from typing import Generic

from madissues_backend.core.shared.domain.entity import EntityId, EntityType, Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.settings import base_dir


def json_encoder(obj):
    if isinstance(obj, GenericUUID):
        return str(obj)
    return obj.dict()


class EntityTable:
    tables: Dict[str, Dict[GenericUUID, Entity]]

    def __init__(self):
        self.tables = {
            'owners': {},
            'organizations': {},
            'faqs': {},
            'students': {},
            'issues': {},
            'issue_comments': {},
            "task_managers": {}
        }

    def save_snapshot(self, name):
        # Get the root path of the project
        root_path = base_dir
        folder_path = os.path.join(root_path, 'db_snapshots')
        os.makedirs(folder_path, exist_ok=True)

        # Save the snapshot in the folder
        file_path = os.path.join(folder_path, name + ".pkl")
        with open(file_path, 'wb') as f:
            pickle.dump(self.tables, f)

    def load_snapshot(self, name):
        # Get the root path of the project
        root_path = base_dir

        # Load the snapshot from the folder
        folder_path = os.path.join(root_path, 'db_snapshots')
        file_path = os.path.join(folder_path, name + ".pkl")
        with open(file_path, 'rb') as f:
            self.tables = pickle.load(f)


class GenericMockRepository(Generic[EntityId, EntityType], metaclass=abc.ABCMeta):
    """An interface for a generic mock repository"""

    def __init__(self, entity_table: EntityTable):
        self.entity_table = entity_table
