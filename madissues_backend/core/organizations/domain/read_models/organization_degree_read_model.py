from pydantic import BaseModel

from madissues_backend.core.organizations.domain.organization_degree import OrganizationDegree


class OrganizationDegreeReadModel(BaseModel):
    id: str
    name: str

    @staticmethod
    def of(degree: OrganizationDegree):
        return OrganizationDegreeReadModel(
            id=str(degree.id),
            name=str(degree.name)
        )
