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
from madissues_backend.core.task_manager.domain.postgres.postgres_task_manager import PostgresTaskManager


class PostgresOrganizationQueryRepository(OrganizationQueryRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all_by_owner(self, owner_id: str) -> List[OrganizationReadModel]:
        organizations = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.teachers),
                     joinedload(PostgresOrganization.courses),
                     joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.owner_id == owner_id).all()
        organization_read_models = [self._map_to_read_model(org) for org in organizations]
        return [self._map_to_read_model(org) for org in organizations]

    def get_by_id(self, id: str) -> OrganizationReadModel:
        organization = (self._session.query(PostgresOrganization)
                        .filter(PostgresOrganization.id == id)
                        .one_or_none()
                        )
        if not organization:
            raise ValueError(f"Organization with id {id} not found")
        else:
            return self._map_to_read_model(organization)

    def get_all_teachers_from_organization(self, id: str) -> List[OrganizationTeacherReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.teachers)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationTeacherReadModel(
            id=str(teacher.id),
            first_name=str(teacher.first_name),
            last_name=str(teacher.last_name),
            email=str(teacher.email),
            office_link=str(teacher.office_link),
            courses=[str(course) for course in teacher.courses]
        ) for teacher in organization.teachers] if organization else []

    def get_all_courses_from_organization(self, id: str) -> List[OrganizationCourseReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.courses)) \
            .filter(PostgresOrganization.id == id).one_or_none()

        return [OrganizationCourseReadModel(
            id=str(course.id),
            name=str(course.name),
            code=str(course.code),
            year=int(course.year),
            icon=str(course.icon),
            primary_color=str(course.primary_color),
            secondary_color=str(course.secondary_color)
        ) for course in organization.courses] if organization else []

    def get_all_degrees_from_organization(self, id: str) -> List[OrganizationDegreeReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationDegreeReadModel(
            id=str(degree.id),
            name=str(degree.name)
        ) for degree in organization.degrees] if organization else []

    def get_all_teachers_degrees_organization(self, id: str) -> list[OrganizationDegreeReadModel]:
        organization = self._session.query(PostgresOrganization) \
            .options(joinedload(PostgresOrganization.degrees)) \
            .filter(PostgresOrganization.id == id).one_or_none()
        return [OrganizationDegreeReadModel(
            id=str(degree.id),
            name=str(degree.name)
        ) for degree in organization.degrees] if organization else []

    def get_organization_task_manager(self, organization_id: str) -> OrganizationTaskManagerReadModel:
        # Buscar un registro en la tabla task_managers según el organization_id
        task_manager_record = self._session.query(
            PostgresTaskManager
        ).filter_by(
            organization_id=organization_id
        ).one_or_none()

        if task_manager_record:
            # Si se encuentra un registro, devolver los datos del task manager
            return OrganizationTaskManagerReadModel(
                task_manager_id=str(task_manager_record.id),
                organization_id=str(task_manager_record.organization_id),
            )
        else:
            # Si no se encuentra ningún registro, devolver None
            return None

    @staticmethod
    def _map_to_read_model(organization: PostgresOrganization) -> OrganizationReadModel:
        # This maps the SQLAlchemy model to a read model, adjusting fields as necessary
        return OrganizationReadModel(
            id=str(organization.id),
            name=str(organization.name),
            logo=str(organization.logo),
            description=str(organization.description),
            contact_info=str(organization.contact_info),
            primary_color=str(organization.primary_color),
            secondary_color=str(organization.secondary_color),
            owner_id=str(organization.owner_id)
        )
