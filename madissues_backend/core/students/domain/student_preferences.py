from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class StudentPreferences(Entity[GenericUUID]):
    theme: str
    language: str
