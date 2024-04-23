from pydantic import BaseModel

from madissues_backend.core.shared.application.event_handler import EventHandler, EventPayload
from madissues_backend.core.users.application.ports.user_repository import UserRepository


class EventPayload(BaseModel):



class CreateTokenWhenUserCreatedEventHandler(EventHandler[]):

    def __init__(self, user_repository : UserRepository):
        self.user_repository = user_repository
