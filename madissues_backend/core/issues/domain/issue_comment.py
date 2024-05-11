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

    def like(self, user_id: GenericUUID):
        self.likes.append(user_id)

    def unlike(self, user_id: GenericUUID):
        self.likes.remove(user_id)

    def is_liked_by(self, user_id: GenericUUID):
        return user_id in self.likes

    def is_response_to(self, comment_id: GenericUUID):
        return self.response_to == comment_id

    def is_author(self, user_id: GenericUUID):
        return self.author == user_id

    def is_issue(self, issue_id: GenericUUID):
        return self.issue_id == issue_id

