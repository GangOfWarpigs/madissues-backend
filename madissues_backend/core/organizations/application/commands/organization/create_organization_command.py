from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, CommandResponse, command_error_handler, \
    owners_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner


class CreateOrganizationCommandRequest(BaseModel):
    name: str
    logo: str | None
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str


class CreateOrganizationCommandResponse(BaseModel):
    owner_id: str
    name: str
    logo: str
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str
    trello_id: str

@owners_only
class CreateOrganizationCommand(Command[CreateOrganizationCommandRequest, CreateOrganizationCommandResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository, storage: StorageService):
        self.authentication_service = authentication_service
        self.repository=repository

    def execute(self, request: CreateOrganizationCommandRequest) -> Response[CreateOrganizationCommandResponse]:
        organization = Organization(
            id=GenericUUID.next_id(),
            owner_id=GenericUUID(self.authentication_service.get_user_id()),
            name=request.name,
            description=request.description,
            contact_info=request.contact_info,
            primary_color=request.primary_color,
            secondary_color=request.secondary_color
        )
        raise NotImplementedError()

