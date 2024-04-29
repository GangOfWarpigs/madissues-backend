from datetime import datetime
from typing import Annotated
from pydantic import Field

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


Content = Annotated[str, Field(min_length=1, max_length=500)]


class IssueComment(Entity[GenericUUID]):
    issue_id: GenericUUID
    author: GenericUUID
    likes: list[GenericUUID]
    content: Content
    date_time: datetime
    response_to: GenericUUID | None
