from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.value_objects import ValueObject

Theme = Annotated[str, Field(pattern=r'^(Dark|Light)$')]
Language = Annotated[str, Field(pattern=r'^[a-zA-Z]{2,3}$')]


class StudentPreferences(ValueObject):
    theme: Theme  # Solo puede ser o Dark o Light
    language: Language  # Solo puede ser un country code

    @staticmethod
    def default():
        return StudentPreferences(
            theme="Dark",
            language="es"
        )
