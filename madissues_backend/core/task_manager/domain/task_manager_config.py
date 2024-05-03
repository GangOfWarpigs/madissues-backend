from typing import Literal

from madissues_backend.core.shared.domain.value_objects import ValueObject


class TaskManagerConfig(ValueObject):
    service: Literal["trello"]
    api_key: str
