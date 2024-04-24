from datetime import datetime

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Issue(AggregateRoot[GenericUUID]):
    title: str
    description: str
    details: str
    proofs: list[str]
    status: str  # Queued, In progress, Solved, Not Solved
    management_id: str
    timestamp: datetime
    course: int
    teachers: list[int]
    student: int
    assigned_to: int
