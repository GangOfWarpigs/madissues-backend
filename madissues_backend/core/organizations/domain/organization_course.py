from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationCourse(Entity[GenericUUID]):
    name: str
    icon: str
    primary_color: str
    secondary_color: str
