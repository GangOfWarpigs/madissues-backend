from pydantic import BaseModel

from madissues_backend.core.faqs.application.ports.faq_repository import FaqRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class GetAllOrganizationFaqsRequest(BaseModel):
    org_id: str


class GetFaqResponse(BaseModel):
    id: str
    question: str
    answer: str
    organization_id: str


@students_only
class GetAllOrganizationFaqsCommand(Command[GetAllOrganizationFaqsRequest, list[GetFaqResponse]]):
    def __init__(self,
                 authentication_service: AuthenticationService,
                 repository: FaqRepository):
        self.authentication_service = authentication_service
        self.repository = repository

    def execute(self, request: GetAllOrganizationFaqsRequest) -> Response[list[GetFaqResponse]]:
        """
        Get a FAQ by its ID
        """

        faqs = self.repository.get_all_organization_faqs(GenericUUID(request.org_id))

        return Response.ok([GetFaqResponse(
            id=str(faq.id),
            question=faq.question,
            answer=faq.answer,
            organization_id=str(faq.organization_id)
        ) for faq in faqs])
