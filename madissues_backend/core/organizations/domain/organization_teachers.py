from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationTeachers(Entity[GenericUUID]):
    first_name: str  # min 1
    last_name: str  # min 1
    email: str | None  # email valid
    office_link: str | None # valid link to serdis
    courses: list[GenericUUID]

