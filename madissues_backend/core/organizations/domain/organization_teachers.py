from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationTeachers(Entity[GenericUUID]):
    first_name: str
    last_name: str
    avatar : str