from typing import Optional, Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.domain.organization_course import OrganizationCourse
from madissues_backend.core.organizations.domain.organization_degree import OrganizationDegree
from madissues_backend.core.organizations.domain.organization_teacher import OrganizationTeacher
from madissues_backend.core.organizations.domain.postgres.postgres_organization import PostgresOrganization
from madissues_backend.core.organizations.domain.postgres.postgres_organization_course import PostgresOrganizationCourse
from madissues_backend.core.organizations.domain.postgres.postgres_organization_degree import PostgresOrganizationDegree
from madissues_backend.core.organizations.domain.postgres.postgres_organization_teacher import \
    PostgresOrganizationTeacher
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class PostgresOrganizationRepository(OrganizationRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, organization: Organization):
        organization_model = self._map_to_model(organization)
        self._session.add(organization_model)
        self._session.commit()

    def remove(self, organization_id: GenericUUID):
        organization_model = self._session.query(PostgresOrganization).filter_by(id=organization_id).one()
        self._session.delete(organization_model)
        self._session.commit()

    def get_by_id(self, organization_id: GenericUUID) -> Optional[Organization]:
        try:
            organization_model = self._session.query(PostgresOrganization).options(
                joinedload(PostgresOrganization.teachers),
                joinedload(PostgresOrganization.courses),
                joinedload(PostgresOrganization.degrees)
            ).filter_by(id=organization_id).one()
            return self._map_to_entity(organization_model)
        except NoResultFound:
            return None

    def save(self, organization: Organization):
        organization_model = self._session.merge(self._map_to_model(organization))
        self._session.commit()

    def exists_with_name(self, name: str) -> bool:
        return self._session.query(
            self._session.query(PostgresOrganization).filter_by(name=name).exists()
        ).scalar()

    def get_by_contact_info(self, contact_info: str) -> Optional[Organization]:
        try:
            organization_model = self._session.query(PostgresOrganization).filter_by(contact_info=contact_info).one()
            return self._map_to_entity(organization_model)
        except NoResultFound:
            return None

    def get_by_name(self, name: str) -> Optional[Organization]:
        try:
            organization_model = self._session.query(PostgresOrganization).filter_by(name=name).one()
            return self._map_to_entity(organization_model)
        except NoResultFound:
            return None

    @staticmethod
    def _map_to_model(organization: Organization) -> PostgresOrganization:
        # Crear modelos para teachers
        teachers_models = [
            PostgresOrganizationTeacher(
                id=teacher.id,
                first_name=teacher.first_name,
                last_name=teacher.last_name,
                email=teacher.email,
                office_link=teacher.office_link,
                organization_id=organization.id,  # Asegurando que el id de la organización se asocie correctamente
                courses=[uuid for uuid in teacher.courses]
            )
            for teacher in organization.teachers
        ]
        # Crear modelos para courses
        courses_models = [
            PostgresOrganizationCourse(
                id=course.id,
                name=course.name,
                code=course.code,
                year=course.year,
                icon=course.icon,
                primary_color=course.primary_color,
                secondary_color=course.secondary_color,
                organization_id=organization.id  # Asegurando que el id de la organización se asocie correctamente
            )
            for course in organization.courses
        ]
        # Crear modelos para degrees
        degrees_models = [
            PostgresOrganizationDegree(
                id=degree.id,
                name=degree.name,
                organization_id=organization.id  # Asegurando que el id de la organización se asocie correctamente
            )
            for degree in organization.degrees
        ]
        # Crear el modelo de Organization
        organization_model = PostgresOrganization(
            id=organization.id,
            owner_id=organization.owner_id,
            name=organization.name,
            logo=organization.logo,
            description=organization.description,
            contact_info=organization.contact_info,
            primary_color=organization.primary_color,
            secondary_color=organization.secondary_color
        )
        # Asociar relaciones
        organization_model.teachers = teachers_models
        organization_model.courses = courses_models
        organization_model.degrees = degrees_models
        return organization_model

    @staticmethod
    def _map_to_entity(organization_model: Type[PostgresOrganization]) -> Organization:
        teachers = [
            OrganizationTeacher(
                id=teacher.id,
                first_name=teacher.first_name,
                last_name=teacher.last_name,
                email=teacher.email,
                office_link=teacher.office_link,
                courses=[uuid for uuid in teacher.courses]
            )
            for teacher in organization_model.teachers
        ]
        courses = [
            OrganizationCourse(
                id=course.id,
                name=course.name,
                code=course.code,
                year=course.year,
                icon=course.icon,
                primary_color=course.primary_color,
                secondary_color=course.secondary_color
            )
            for course in organization_model.courses
        ]
        degrees = [
            OrganizationDegree(
                id=degree.id,
                name=degree.name
            )
            for degree in organization_model.degrees
        ]
        return Organization(
            id=organization_model.id,
            owner_id=organization_model.owner_id,
            name=organization_model.name,
            logo=organization_model.logo,
            description=organization_model.description,
            contact_info=organization_model.contact_info,
            primary_color=organization_model.primary_color,
            secondary_color=organization_model.secondary_color,
            teachers=teachers,
            courses=courses,
            degrees=degrees
        )
