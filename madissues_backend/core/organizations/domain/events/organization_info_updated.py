from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class OrganizationInfoUpdatedPayload(BaseModel):
    id: str
    name: str
    description: str
    primary_color: str
    secondary_color: str


class OrganizationInfoUpdated(DomainEvent[OrganizationInfoUpdatedPayload]):
    name: str = "@organization/info_updated"
