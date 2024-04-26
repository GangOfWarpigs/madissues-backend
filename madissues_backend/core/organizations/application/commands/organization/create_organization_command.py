from pydantic import BaseModel
from madissues_backend.core.shared.application.command import Command, CommandResponse, command_error_handler
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner


class CreateOrganizationCommandRequest(BaseModel):
    owner_id: str
    name: str
    logo: str
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str
    banner: str
    trello_id: str


class CreateOrganizationCommandResponse(BaseModel):
    organization_id: str


class CreateOrganizationCommand(Command[CreateOrganizationCommandRequest, CreateOrganizationCommandResponse]):

    def __init__(self, owner_repository: OwnerRepository, organization_repository: OrganizationRepository,
                 token_generator: TokenGenerator):
        self.owner_repository = owner_repository
        self.organization_repository = organization_repository
        self.token_generator = token_generator

    @command_error_handler
    def execute(self, request: CreateOrganizationCommandRequest) -> Response[CreateOrganizationCommandResponse]:
        owner = self.owner_repository.get_by_id(GenericUUID(request.owner_id))
        if not owner:
            return Response.fail(message="Owner not found")

        # Check if the owner has permission to create organizations
        if not self.has_permission_to_create_organization(owner):
            return Response.fail(message="Owner does not have permission to create organizations")

        organization = Organization(
            id=GenericUUID.next_id(),
            name=request.name,
            logo=request.logo,
            description=request.description,
            contact_info=request.contact_info,
            primary_color=request.primary_color,
            secondary_color=request.secondary_color,
            banner=request.banner,
            trello_id=request.trello_id
        )

        self.organization_repository.add(organization)

        return Response.ok(
            CreateOrganizationCommandResponse(
                organization_id=str(organization.id)
            )
        )

    def has_permission_to_create_organization(self, owner: Owner) -> bool:
        # Here you can implement any logic to determine if the owner has permission to create organizations
        # For example, you could check if the owner has a certain role or privilege
        # For now, let's assume all owners have permission to create organizations
        return True
