from fastapi import APIRouter
from madissues_backend.apps.rest_api.dependencies import owner_repository, password_hasher, token_generator
from madissues_backend.core.owners.application.commands.sign_in_owner_command import SignInOwnerCommandRequest, \
    SignInOwnerCommandResponse, SignInOwnerCommand
from madissues_backend.core.owners.application.commands.sign_up_owner_command import SignUpOwnerCommand, \
    SignUpOwnerCommandRequest, SignUpOwnerCommandResponse
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/owners/signup", tags=["owners"])
def signup_owners(request: SignUpOwnerCommandRequest) -> Response[SignUpOwnerCommandResponse]:
    command = SignUpOwnerCommand(owner_repository, password_hasher, token_generator)
    return command.run(request)


@router.post("/owners/signin", tags=["owners"])
def signin_owners(request: SignInOwnerCommandRequest) -> Response[SignInOwnerCommandResponse]:
    command = SignInOwnerCommand(owner_repository, password_hasher)
    return command.run(request)
