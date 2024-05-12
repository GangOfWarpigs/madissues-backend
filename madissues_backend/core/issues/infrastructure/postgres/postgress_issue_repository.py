from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List, Type

from madissues_backend.core.issues.application.ports.issue_repository import IssueRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.infrastructure.postgres.models.issue_model import PostgresIssueModel
# Import the sqlalchemy model


from madissues_backend.core.shared.domain.value_objects import GenericUUID


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

    @staticmethod
    def map_to_entity(model: Type[PostgresIssueModel]) -> Issue:
        return Issue(
            id=model.id,
            title=model.title,
            description=model.description,
            details=model.details,
            proofs=model.proofs,
            status=model.status,
            date_time=model.date_time,
            course=model.course,
            teachers=model.teachers,
            student_id=model.student_id,
            organization_id=model.organization_id
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

    def exists_with_name(self, name: str) -> bool:
        return self._session.query(
            self._session.query(PostgresIssueModel).filter(PostgresIssueModel.title == name).exists()).scalar()

    def get_by_name(self, name: str) -> Optional[Issue]:
        return self._session.query(PostgresIssueModel).filter(PostgresIssueModel.title == name).first()

    def get_all(self) -> List[Issue]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).all()]

    def get_all_by_course(self, course_id: GenericUUID) -> List[Issue]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).filter(
            PostgresIssueModel.course == course_id).all()]

    def get_all_by_student(self, student_id: GenericUUID) -> List[Issue]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(PostgresIssueModel.student_id == student_id).all()]

    def get_all_by_teacher(self, teacher_id: GenericUUID) -> List[Issue]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(
                    PostgresIssueModel.teachers.contains([teacher_id])).all()]

    def get_all_by_status(self, status: str) -> List[Issue]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(PostgresIssueModel.status == status).all()]
