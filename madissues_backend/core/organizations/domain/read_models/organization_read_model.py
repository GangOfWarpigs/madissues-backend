from pydantic import BaseModel

from madissues_backend.core.organizations.domain.organization import Organization


class OrganizationReadModel(BaseModel):
    id: str
    owner_id: str
    name: str
    logo: str | None
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str

    @staticmethod
    def of(organization: Organization):
        return OrganizationReadModel(
            id=str(organization.id),
            owner_id=str(organization.owner_id),
            name=organization.name,
            logo=organization.logo,
            description=organization.description,
            contact_info=organization.contact_info,
            primary_color=organization.primary_color,
            secondary_color=organization.secondary_color
        )
