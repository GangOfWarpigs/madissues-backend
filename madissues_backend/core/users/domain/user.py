from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import Email

class User(AggregateRoot):
    email : Email
    first_name : str
    last_name : str
    password : str

