from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Issue(AggregateRoot[GenericUUID]):
    title: str
    description: str
    details: str
    proofs: list[str]
    status: str

    course: int
    teachers: list[int]
    student: int
    assigned_to: int

