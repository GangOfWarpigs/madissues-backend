from pydantic import BaseModel

from madissues_backend.core.faqs.application.ports.faq_repository import FaqRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class GetFaqRequest(BaseModel):
    faq_id: str


class GetFaqResponse(BaseModel):
    id: str
    question: str
    answer: str
    organization_id: str


@students_only
class GetFaqCommand(Command[GetFaqRequest, GetFaqResponse]):
    def __init__(self,
                 authentication_service: AuthenticationService,
                 repository: FaqRepository):
        self.authentication_service = authentication_service
        self.repository = repository

    def execute(self, request: GetFaqRequest) -> Response[GetFaqResponse]:
        """
        Get a FAQ by its ID
        """

        faq = self.repository.get_by_id(GenericUUID(request.faq_id))

        if not faq:
            raise Exception("FAQ not found")

        return Response.ok(GetFaqResponse(
            id=str(faq.id),
            question=faq.question,
            answer=faq.answer,
            organization_id=str(faq.organization_id)
        ))
