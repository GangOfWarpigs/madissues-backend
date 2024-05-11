from typing import Literal, Annotated
from pydantic import Field, AfterValidator

from madissues_backend.core.shared.domain.value_objects import ValueObject


valid_services=["trello"]
def is_valid_service(service):
    if service not in valid_services: raise ValueError("Service must be one of " + str(valid_services))
    return service


class TaskManagerConfig(ValueObject):
    service: Annotated[str, AfterValidator(is_valid_service)]
    api_key: Annotated[str, Field(min_length=1)]
    api_token: Annotated[str, Field(min_length=1)]
