from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Name = Annotated[str, Field(min_length=1, max_length=280)]
Description = Annotated[str, Field(min_length=1, max_length=280)]
LinkToImage = Annotated[str, Field(min_length=1, pattern=r'^.*\.(png|jpe?g)$')]
HexadecimalColor = Annotated[str, Field(min_length=1, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')]
ContactInfo = Annotated[str, Field(min_length=1, max_length=80)]


class Organization(AggregateRoot[GenericUUID]):
    name: Name   # Mayor a 1
    logo: LinkToImage  # Link a una image
    description: Description  # Mayor a 1, maxim 280
    contact_info: ContactInfo  # Mayor a 1, maxim 80
    primary_color: HexadecimalColor  # hexadecimal valid
    secondary_color: HexadecimalColor  # hexadecimal valid
    banner: LinkToImage  # Link a una image

    trello_id: GenericUUID




