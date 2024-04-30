from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import ValueObject


class OwnerTaskManager(ValueObject):
    name : str
    token: str
