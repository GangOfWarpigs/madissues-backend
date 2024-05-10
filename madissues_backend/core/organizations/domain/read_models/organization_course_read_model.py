from typing import Annotated

from pydantic import Field, BaseModel

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.domain.value_objects import GenericUUID, LinkToImage

class OrganizationCourseReadModel(BaseModel):
    name: str
    code: str
    icon: str
    primary_color: str
    secondary_color: str

