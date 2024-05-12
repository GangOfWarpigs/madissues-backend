from sqlalchemy.orm import Session
from typing import Optional, List, Type

from madissues_backend.core.issues.application.ports.issue_query_repository import IssueQueryRepository
from madissues_backend.core.issues.domain.issue import Issue
from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel
from madissues_backend.core.issues.domain.postgres.issue_model import PostgresIssueModel


# Import the sqlalchemy model


class PostgresIssueQueryRepository(IssueQueryRepository):
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
    def map_to_entity(model: Type[PostgresIssueModel]) -> IssueReadModel:
        print("CALL TO MAP TO ENTITY ------------------------->")
        read_model = IssueReadModel(
            title=str(model.title),
            description=str(model.description),
            details=str(model.details),
            proofs=[str(proof) for proof in model.proofs] if model.proofs is not None else [],
            status=str(model.status),
            date_time=model.date_time.strftime("%Y-%m-%d %H:%M:%S") if model.date_time else '',
            course=str(model.course),
            teachers=[str(teacher) for teacher in model.teachers] if model.teachers else [],
            student_id=str(model.student_id),
            student=None
        )
        print("READ MODEL ------------------------->")
        print(read_model)
        return read_model

    def get_by_id(self, id: str) -> Optional[IssueReadModel]:
        return self._session.query(PostgresIssueModel).filter(PostgresIssueModel.id == id).first()

    def exists_with_name(self, name: str) -> bool:
        return self._session.query(
            self._session.query(PostgresIssueModel).filter(PostgresIssueModel.title == name).exists()).scalar()

    def get_by_name(self, name: str) -> Optional[IssueReadModel]:
        return self._session.query(PostgresIssueModel).filter(PostgresIssueModel.title == name).first()

    def get_all(self) -> List[IssueReadModel]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).all()]

    def get_all_by_course(self, course_id: str) -> List[IssueReadModel]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).filter(
            PostgresIssueModel.course == course_id).all()]

    def get_all_by_student(self, student_id: str) -> List[IssueReadModel]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(PostgresIssueModel.student_id == student_id).all()]

    def get_all_by_teacher(self, teacher_id: str) -> List[IssueReadModel]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(
                    PostgresIssueModel.teachers.contains([teacher_id])).all()]

    def get_all_by_status(self, status: str) -> List[IssueReadModel]:
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(PostgresIssueModel.status == status).all()]

    def get_all_by_organization(self, organization_id: str) -> List[IssueReadModel]:
        print("organization_id", organization_id)
        return [self.map_to_entity(model) for model in
                self._session.query(PostgresIssueModel).filter(
                    PostgresIssueModel.organization_id == organization_id).all()]

    def get_all_by_title(self, title: str) -> list[IssueReadModel]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).filter(
            PostgresIssueModel.title == title).all()]

    def get_all_by_date_greater_than(self, date: str) -> list[IssueReadModel]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).filter(
            PostgresIssueModel.date_time > date).all()]

    def get_all_by_date_less_than(self, date: str) -> list[IssueReadModel]:
        return [self.map_to_entity(model) for model in self._session.query(PostgresIssueModel).filter(
            PostgresIssueModel.date_time < date).all()]

