from typing import Literal

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Card(Entity[GenericUUID]):
    task_manager_id: str
    status: Literal["Queued", "In progress", "Solved", "Not solved"]