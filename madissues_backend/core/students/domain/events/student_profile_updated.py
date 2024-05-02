from pydantic import BaseModel
from madissues_backend.core.shared.domain.events import DomainEvent


class StudentProfileUpdatedPayload(BaseModel):
    user_id: str
    degree: str
    joined_courses: list[str]


class StudentProfileUpdated(DomainEvent[StudentProfileUpdatedPayload]):
    name: str = "@student/profile_updated"
