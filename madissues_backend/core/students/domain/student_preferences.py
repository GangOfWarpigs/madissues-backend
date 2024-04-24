from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class StudentPreferences(Entity[GenericUUID]):
    theme: str  # Solo puede ser o Dark o Light
    language: str  # Solo puede ser un country code
