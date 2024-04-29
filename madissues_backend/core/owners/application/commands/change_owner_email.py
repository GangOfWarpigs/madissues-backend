from pydantic import BaseModel

from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class ChangeOwnerEmailRequest(BaseModel):
    email: str


class ChangeOwnerEmailResponse(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone_number: str


@owners_only
class ChangeOwnerEmailCommand(Command[ChangeOwnerEmailRequest, ChangeOwnerEmailResponse]):
    def __init__(self, authentication_service: AuthenticationService, owner_repository: OwnerRepository, event_bus: EventBus):
        self.authentication_service = authentication_service
        self.owner_repository = owner_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeOwnerEmailRequest) -> Response[ChangeOwnerEmailResponse]:
        owner_id = self.authentication_service.get_user_id()
        owner = self.owner_repository.get_by_id(GenericUUID(owner_id))
        owner.change_email(request.email)
        self.owner_repository.save(owner)
        self.event_bus.notify(owner.collect_events())
        return Response.ok(ChangeOwnerEmailResponse(
            email=owner.email,
            first_name=owner.first_name,
            last_name=owner.last_name,
            phone_number=owner.phone_number
        ))
