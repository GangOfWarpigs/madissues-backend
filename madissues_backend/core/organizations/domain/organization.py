from typing import Annotated
from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


Description = Annotated[str, Field(max_length=280, min_length=1)]

class Organization(AggregateRoot[GenericUUID]):
    name: str  # Mayor a 1
    logo: str  # Link a una image
    description: Description  # Mayor a 1, maxim 280
    contact_info: str  # Mayor a 1, maxim 80
    primary_color: str  # hexadecimal valid
    secondary_color: str  # hexadecimal valid
    banner: str  # Link a una image

    trello_id: GenericUUID

