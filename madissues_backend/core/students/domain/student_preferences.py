from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID

from typing import Annotated
from pydantic import Field

Theme = Annotated[str, Field(pattern=r'^(Dark|Light)$')]
Language = Annotated[str, Field(pattern=r'^[a-zA-Z]{2,3}$')]


class StudentPreferences(Entity[GenericUUID]):
    theme: Theme  # Solo puede ser o Dark o Light
    language: Language  # Solo puede ser un country code
