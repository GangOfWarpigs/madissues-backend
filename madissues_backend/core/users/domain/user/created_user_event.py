from pydantic import BaseModel

from madissues_backend.core.shared.domain.events import DomainEvent


class Payload(BaseModel):
    user_id: str
    email: str


class CreatedUserDomainEvent(DomainEvent[Payload]):
    name = "user/user_created"
