from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentPersonalDataUpdatedPayload(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    started_studies_date: str


class StudentPersonalDataUpdated(DomainEvent[StudentPersonalDataUpdatedPayload]):
    name: str = "@student/personal_data_updated"
