from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class StudentPreferencesUpdatedPayload(BaseModel):
    user_id: str
    language: str
    theme: str


class StudentPreferencesUpdated(DomainEvent[StudentPreferencesUpdatedPayload]):
    name: str = "@student/preferences_updated"
