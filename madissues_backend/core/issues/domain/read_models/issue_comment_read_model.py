from pydantic import BaseModel

from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.issue_comment import IssueComment


class IssueCommentReadModel(BaseModel):
    issue_id: str
    author: str
    likes: list[str]
    content: str
    date_time: str
    response_to: str | None

    @staticmethod
    def of(issue_comment: IssueComment) -> 'IssueCommentReadModel':
        return IssueCommentReadModel(
            issue_id=str(issue_comment.issue_id),
            author=str(issue_comment.author),
            likes=[str(like) for like in issue_comment.likes],
            content=issue_comment.content,
            date_time=issue_comment.date_time.strftime('%Y-%m-%d'),
            response_to=str(issue_comment.response_to) if issue_comment.response_to is not None else None
        )
