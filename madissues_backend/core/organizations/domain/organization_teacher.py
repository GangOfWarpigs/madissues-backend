from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Name = Annotated[str, Field(min_length=1, max_length=80)]
Email = Annotated[str, Field(min_length=5, max_length=200, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')]
LinkToDis = Annotated[str, Field(min_length=1, pattern=r'^https://www.dis.ulpgc.es/.*$')]


class OrganizationTeacher(Entity[GenericUUID]):
    first_name: Name  # min 1
    last_name: Name  # min 1
    email: Email | None  # email valid
    office_link: LinkToDis | None  # valid link to dis.ulpgc.es
    courses: list[GenericUUID]

