from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, event_bus, faq_repository
from madissues_backend.core.faqs.application.commands.create_faq_command import CreateFaqRequest, CreateFaqCommand, CreateFaqResponse
from madissues_backend.core.faqs.application.commands.get_all_organization_faqs_command import GetAllOrganizationFaqsCommand, \
    GetAllOrganizationFaqsRequest
from madissues_backend.core.faqs.application.commands.get_faq_command import GetFaqResponse, GetFaqCommand, GetFaqRequest
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/faqs/", tags=["faqs"])
def create_faq(request: CreateFaqRequest, token: Annotated[str, Header()]) -> Response[CreateFaqResponse]:
    authorization = authorization_service(token)
    command = CreateFaqCommand(authorization, faq_repository, event_bus)
    return command.run(request)


@router.get("/faqs/organization/{org_id}", tags=["faqs"])
def get_all_organization_faqs(org_id: str, token: Annotated[str, Header()]) -> Response[list[GetFaqResponse]]:
    authorization = authorization_service(token)
    command = GetAllOrganizationFaqsCommand(authorization, faq_repository)
    return command.run(GetAllOrganizationFaqsRequest(org_id=org_id))


@router.get("/faqs/{faq_id}", tags=["faqs"])
def get_faq(faq_id: str, token: Annotated[str, Header()]) -> Response[GetFaqResponse]:
    authorization = authorization_service(token)
    command = GetFaqCommand(authorization, faq_repository)
    return command.run(GetFaqRequest(faq_id=faq_id))
