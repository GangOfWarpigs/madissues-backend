from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.postgres.issue_model import PostgresIssueModel
from madissues_backend.core.shared.domain.value_objects import GenericUUID


# Import the sqlalchemy model


class PostgresIssueRepository(IssueRepository):
    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def map_to_model(entity: Issue) -> PostgresIssueModel:
        return PostgresIssueModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            details=entity.details,
            proofs=entity.proofs,
            status=entity.status,
            date_time=entity.date_time,
            course=entity.course,
            teachers=entity.teachers,
            student_id=entity.student_id,
            organization_id=entity.organization_id
        )

    def add(self, issue: Issue) -> None:
        self._session.add(PostgresIssueRepository.map_to_model(issue))
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e

    def remove(self, id: GenericUUID) -> None:
        issue = self.get_by_id(id)
        if issue:
            self._session.delete(issue)
            self._session.commit()

    def get_by_id(self, id: GenericUUID) -> Optional[Issue]:
        return self._session.query(PostgresIssueModel).filter(PostgresIssueModel.id == id).first()

    def save(self, issue: Issue) -> None:
        try:
            self._session.get(PostgresIssueModel, issue.id)
            self._session.merge(PostgresIssueRepository.map_to_model(issue))
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e
