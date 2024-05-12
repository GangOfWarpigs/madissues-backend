from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.organizations.domain.postgres.postgres_organization import PostgresOrganization
from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_degree_read_model import \
    OrganizationDegreeReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.organizations.domain.read_models.organization_task_manager_read_model import \
    OrganizationTaskManagerReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel


class PostgresOrganizationQueryRepository(OrganizationQueryRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all_by_owner(self, owner_id: str) -> List[OrganizationReadModel]:
        organizations = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.teachers),
                     joinedload(PostgresOrganization.courses),
                     joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.owner_id == owner_id).all()
        return [self._map_to_read_model(org) for org in organizations]

    def get_by_id(self, id: str) -> OrganizationReadModel:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.teachers),
                     joinedload(PostgresOrganization.courses),
                     joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return self._map_to_read_model(organization) if organization else None

    def get_all_teachers_from_organization(self, id: str) -> List[OrganizationTeacherReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.teachers)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationTeacherReadModel(
            id=teacher.id,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            email=teacher.email,
            office_link=teacher.office_link,
            courses=teacher.courses
        ) for teacher in organization.teachers] if organization else []

    def get_all_courses_from_organization(self, id: str) -> List[OrganizationCourseReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.courses)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationCourseReadModel(
            id=course.id,
            name=course.name,
            code=course.code,
            year=course.year,
            icon=course.icon,
            primary_color=course.primary_color,
            secondary_color=course.secondary_color
        ) for course in organization.courses] if organization else []

    def get_all_degrees_from_organization(self, id: str) -> List[OrganizationDegreeReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationDegreeReadModel(
            id=degree.id,
            name=degree.name
        ) for degree in organization.degrees] if organization else []

    def get_all_teachers_degrees_organization(self, id: str) -> list[OrganizationDegreeReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationDegreeReadModel(
            id=degree.id,
            name=degree.name
        ) for degree in organization.degrees] if organization else []

    def get_organization_task_manager(self, id: str) -> OrganizationTaskManagerReadModel:
        # FIXME: Must search in the task manager table
        # Assuming that we need to fetch complex task management data:
        organization = self._session.query(PostgresOrganization).filter(PostgresOrganization.id == id).one_or_none()
        if organization:
            # Assuming there is a method to fetch task manager data
            return OrganizationTaskManagerReadModel(
                # hypothetical fields based on possible task management details
                task_manager_id='1234',
                organization_id=organization.id,
                tasks=[]  # List of tasks, for example
            )
        return None

    @staticmethod
    def _map_to_read_model(organization: PostgresOrganization) -> OrganizationReadModel:
        # This maps the SQLAlchemy model to a read model, adjusting fields as necessary
        return OrganizationReadModel(
            id=str(organization.id),
            name=organization.name,
            description=organization.description,
            contact_info=organization.contact_info,
            primary_color=organization.primary_color,
            secondary_color=organization.secondary_color,
            owner_id=str(organization.owner_id)
        )
