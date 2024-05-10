from pydantic import Field, BaseModel


class OrganizationTeacher(BaseModel):
    id : str
    first_name: str  # min 1
    last_name: str  # min 1
    email: str  # email valid
    office_link: str | None
    courses: list[str]
