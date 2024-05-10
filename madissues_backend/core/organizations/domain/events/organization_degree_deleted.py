from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationDegreeDeletedPayload(BaseModel):
    id: str
    organization_id: str


class OrganizationDegreeDeleted(DomainEvent[OrganizationDegreeDeletedPayload]):
    name: str = "@organization/degree_deleted"
