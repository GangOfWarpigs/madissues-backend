from pydantic import BaseModel


class OrganizationReadModel(BaseModel):
    id: str
    owner_id: str
    name: str
    logo: str
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str
