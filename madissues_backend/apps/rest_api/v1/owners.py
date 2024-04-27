from fastapi import APIRouter

from madissues_backend.apps.rest_api.dependencies import owner_repository, password_hasher, token_generator
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommand, \
    SignUpOwnerCommandRequest, SignUpOwnerCommandResponse
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/owners/signup", tags=["owners"])
def signup_owners(request: SignUpOwnerCommandRequest) -> Response[SignUpOwnerCommandResponse]:
    command = SignUpOwnerCommand(owner_repository, password_hasher, token_generator)
    return command.execute(request)
