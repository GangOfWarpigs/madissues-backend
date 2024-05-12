from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Type

from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.issues.infrastructure.postgres.models.issue_comment_model import PostgresIssueCommentModel
from madissues_backend.core.issues.infrastructure.postgres.models.issue_model import PostgresIssueModel
# Import the sqlalchemy model


from madissues_backend.core.shared.domain.value_objects import GenericUUID


class PostgresIssueCommentRepository(IssueCommentRepository):
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def map_to_model(entity: IssueComment) -> PostgresIssueModel:
        return PostgresIssueCommentModel(
            id=entity.id,
            issue_id=entity.issue_id,
            author_id=entity.author,
            likes=entity.likes,
            content=entity.content,
            date_time=entity.date_time,
            response_to=entity.response_to
        )

    def add(self, issue_comment: IssueComment):
        self._session.add(PostgresIssueCommentRepository.map_to_model(issue_comment))
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e

    def remove(self, issue_id: GenericUUID):
        issue = self.get_by_id(issue_id)
        if issue:
            self._session.delete(issue)
            self._session.commit()

    def get_by_id(self, issue_id: GenericUUID) -> IssueComment | None:
        return self._session.query(PostgresIssueModel).filter(PostgresIssueModel.id == issue_id).first()

    def save(self, entity: IssueComment):
        try:
            self._session.get(PostgresIssueModel, entity.id)
            self._session.merge(PostgresIssueCommentRepository.map_to_model(entity))
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e
