from typing import Annotated

from pydantic import Field

from madissues_backend.core.organizations.domain.organization_task_manager import OrganizationTaskManager
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.task_manager import TaskManager
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Name = Annotated[str, Field(min_length=1, max_length=280)]
Description = Annotated[str, Field(min_length=1, max_length=280)]
LinkToImage = Annotated[str, Field(min_length=1, pattern=r'^.*\.(png|jpe?g)$')]
HexadecimalColor = Annotated[str, Field(min_length=1, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')]
ContactInfo = Annotated[str, Field(min_length=1, max_length=80)]


class Organization(AggregateRoot[GenericUUID]):
    owner_id: GenericUUID
    name: Name   # Mayor a 1
    logo: LinkToImage  # Link a una image
    description: Description  # Mayor a 1, maxim 280
    contact_info: ContactInfo  # Mayor a 1, maxim 80
    primary_color: HexadecimalColor  # hexadecimal valid
    secondary_color: HexadecimalColor  # hexadecimal valid
    board_id: str
    task_manager: OrganizationTaskManager | None = Field(init=False, default=None)

    def integrate_task_manager(self, task_manager: TaskManager, api_token):
        self.task_manager = OrganizationTaskManager(
            task_manager_name=task_manager,
            token=api_token
        )
