from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationCourse(Entity[GenericUUID]):
    name: str  # min 2, maxim 60
    code: str  # min 2 max 8
    icon: str  # image valida
    primary_color: str  # hexadecimal valid
    secondary_color: str  # hexadecimal valid

