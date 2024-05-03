from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationDegree(Entity[GenericUUID]):
    name: str
