from abc import ABC, abstractmethod

from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel


class OrganizationQueryRepository(ABC):
    @abstractmethod
    def get_all_by_owner(self, owner_id: str) -> list[OrganizationReadModel]:
        ...

    @abstractmethod
    def get_by_id(self, id: str) -> OrganizationReadModel:
        ...

    @abstractmethod
    def get_all_teachers_from_organization(self, id: str) -> list[OrganizationTeacherReadModel]:
        ...

    @abstractmethod
    def get_all_courses_from_organization(self, id: str) -> list[OrganizationCourseReadModel]:
        ...
