from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Organization(AggregateRoot[GenericUUID]):
    name: str
    logo: str
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str

    trello_id: int
