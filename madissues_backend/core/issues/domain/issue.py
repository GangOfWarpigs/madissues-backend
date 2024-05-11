from datetime import datetime
from typing import Annotated

from pydantic import Field

from madissues_backend.core.issues.domain.events.issue_status_updated import IssueStatusUpdated, \
    IssueStatusUpdatedPayload
from madissues_backend.core.organizations.domain.organization import LinkToImage, Description
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID

Title = Annotated[str, Field(min_length=2, max_length=80)]
Details = Annotated[str, Field(min_length=2, max_length=1000)]
Status = Annotated[str, Field(min_length=1, max_length=20, pattern=r'^(Queued|In progress|Solved|Not Solved)$')]


class Issue(AggregateRoot[GenericUUID]):
    title: Title
    description: Description
    details: Details
    proofs: list[LinkToImage]  # List of image links
    status: Status  # Queued, In progress, Solved, Not Solved
    date_time: datetime
    course: GenericUUID
    teachers: list[GenericUUID]
    student_id: GenericUUID
    organization_id: GenericUUID

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