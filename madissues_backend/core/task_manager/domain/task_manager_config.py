from typing import Literal, Annotated
from pydantic import Field

from madissues_backend.core.shared.domain.value_objects import ValueObject


class TaskManagerConfig(ValueObject):
    service: str
    api_key: Annotated[str, Field(min_length=1)]
