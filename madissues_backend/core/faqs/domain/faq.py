from datetime import datetime

from madissues_backend.core.faqs.domain.events.faq_updated import FaqUpdatedPayload, FaqUpdated
from madissues_backend.core.issues.domain.events.issue_info_updated import IssueInfoUpdatedPayload, IssueInfoUpdated
from madissues_backend.core.issues.domain.events.issue_status_updated import IssueStatusUpdated, \
    IssueStatusUpdatedPayload
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Faq(AggregateRoot[GenericUUID]):
    id: GenericUUID
    organization_id: GenericUUID
    question: str
    answer: str

    def update_answer(self, new_answer: str) -> None:
        self.answer = new_answer

        # Validate the fields
        self.validate_field("answer", self.answer)

        # Register and dispatch the event
        self.register_event(
            FaqUpdated(
                payload=FaqUpdatedPayload(
                    id=str(self.id),
                    question=self.question,
                    answer=self.answer,
                    organization_id=str(self.organization_id),
                )
            )
        )

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.date_time = datetime.now()

        # Validate the fields
        self.validate_field("status", self.status)
        self.validate_field("date_time", self.date_time)

        # Register and dispatch the event
        self.register_event(
            IssueStatusUpdated(
                payload=IssueStatusUpdatedPayload(
                    issue_id=str(self.id),
                    new_status=new_status
                )
            )
        )

    def update_information(self, title: str, description: str, details: str, proofs: list[str], teachers: list[str]) -> None:
        self.title = title
        self.description = description
        self.details = details
        self.proofs = proofs
        self.teachers = [GenericUUID(teacher) for teacher in teachers]

        # Validate the fields
        self.validate_field("title", self.title)
        self.validate_field("description", self.description)
        self.validate_field("details", self.details)
        self.validate_field("proofs", self.proofs)
        self.validate_field("teachers", self.teachers)

        # Register and dispatch the event
        self.register_event(
            IssueInfoUpdated(
                payload=IssueInfoUpdatedPayload(
                    issue_id=str(self.id),
                    title=title,
                    description=description,
                    details=details,
                    proofs=proofs,
                    teachers=teachers
                )
            )
        )
