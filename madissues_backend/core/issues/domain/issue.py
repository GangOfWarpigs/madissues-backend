from datetime import datetime

from madissues_backend.core.organizations.domain.organization import LinkToImage, Description
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Issue(AggregateRoot[GenericUUID]):
    title: str
    description: Description
    details: str
    proofs: list[LinkToImage]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    timestamp: datetime
    course: GenericUUID
    teachers: list[GenericUUID]
    student: GenericUUID
    task_manager_id: GenericUUID
    assigned_to: GenericUUID
