from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID, LinkToImage

Name = Annotated[str, Field(min_length=2, max_length=60)]
Code = Annotated[str, Field(min_length=2, max_length=8)]
HexadecimalColor = Annotated[str, Field(min_length=1, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')]


class OrganizationCourse(Entity[GenericUUID]):
    name: Name
    code: Code
    icon: LinkToImage
    primary_color: HexadecimalColor
    secondary_color: HexadecimalColor

