from pydantic import BaseModel

from madissues_backend.core.faqs.application.ports.faq_repository import FaqRepository
from madissues_backend.core.faqs.domain.events.faq_created import FaqCreatedPayload, FaqCreated
from madissues_backend.core.faqs.domain.faq import Faq
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class CreateFaqRequest(BaseModel):
    question: str
    answer: str
    organization_id: str


class CreateFaqResponse(BaseModel):
    id: str
    question: str
    answer: str
    organization_id: str


@owners_only
class CreateFaqCommand(Command[CreateFaqRequest, CreateFaqResponse]):
    def __init__(self,
                 repository: FaqRepository,
                 event_bus: EventBus):
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: CreateFaqRequest) -> Response[CreateFaqResponse]:
        """
            - Must create a faq associated with the organization
        """

        faq = Faq(
            id=GenericUUID.next_id(),
            answer=request.answer,
            question=request.question,
            organization_id=GenericUUID(request.organization_id)
        )

        faq.register_event(FaqCreated(
            payload=FaqCreatedPayload(
                id=str(faq.id),
                question=faq.question,
                answer=faq.answer,
                organization_id=str(faq.organization_id)
            )
        ))

        self.repository.add(faq)

        self.event_bus.notify_all(faq.collect_events())

        return Response.ok(CreateFaqResponse(
            id=str(faq.id),
            question=faq.question,
            answer=faq.answer,
            organization_id=str(faq.organization_id)
        ))
