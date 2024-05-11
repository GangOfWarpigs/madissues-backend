from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_degree_read_model import \
    OrganizationDegreeReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.organizations.domain.read_models.organization_task_manager_read_model import \
    OrganizationTaskManagerReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockOrganizationQueryRepository(OrganizationQueryRepository):

    def __init__(self, db: EntityTable):
        self.db = db

    def get_all_courses_from_organization(self, id: str) -> list[OrganizationCourseReadModel]:
        organization: Organization = self.db.tables["organizations"].get(GenericUUID(id))
        return list(OrganizationCourseReadModel.of(x) for x in organization.courses)

    def get_all_teachers_from_organization(self, id: str) -> list[OrganizationTeacherReadModel]:
        organization: Organization = self.db.tables["organizations"].get(GenericUUID(id))
        return list(OrganizationTeacherReadModel.of(x) for x in organization.teachers)

    def get_all_teachers_degrees_organization(self, id: str) -> list[OrganizationDegreeReadModel]:
        organization: Organization = self.db.tables["organizations"].get(GenericUUID(id))
        return list(OrganizationDegreeReadModel.of(x) for x in organization.degrees)

    def get_all_by_owner(self, owner_id: str):
        organizations_map: dict[GenericUUID, Organization] = self.db.tables["organizations"]
        return list(OrganizationReadModel.of(x) for x in organizations_map.values() if str(x.owner_id) == owner_id)

    def get_by_id(self, id: str):
        organization: Organization = self.db.tables["organizations"].get(GenericUUID(id))
        if organization is None:
            return None
        return OrganizationReadModel.of(organization)

    def get_organization_task_manager(self, id: str) -> OrganizationTaskManagerReadModel:
        organization: Organization = self.db.tables["organizations"][GenericUUID(id)]
        task_managers = self.db.tables["task_managers"]

        for task_manager in task_managers.values():
            if task_manager.organization_id == organization.id:
                return OrganizationTaskManagerReadModel.of(organization, task_manager.task_manager_project_id)
        return None

