from datetime import datetime

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IssueComment(Entity[GenericUUID]):
    issue_id: GenericUUID
    author: int
    likes: list[int]
    content: str
    timestamp: datetime
    response_to: int | None
