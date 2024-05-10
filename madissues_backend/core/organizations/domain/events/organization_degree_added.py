from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationDegreeAddedPayload(BaseModel):
    id: str
    organization_id: str
    name: str


class OrganizationDegreeAdded(DomainEvent[OrganizationDegreeAddedPayload]):
    name: str = "@organization/degree_created"
