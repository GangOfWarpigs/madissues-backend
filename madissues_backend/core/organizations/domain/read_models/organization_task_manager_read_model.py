from pydantic import BaseModel

from madissues_backend.core.organizations.domain.organization import Organization


class OrganizationTaskManagerReadModel(BaseModel):
    organization_id: str
    task_manager_id: str

    @staticmethod
    def of(organization: Organization, task_manager_id: str):
        return OrganizationTaskManagerReadModel(
            organization_id=str(organization.id),
            task_manager_id=str(task_manager_id)
        )
