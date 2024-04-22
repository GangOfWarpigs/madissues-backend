from madissues_backend.core.shared.domain.entity import Entity

class User(Entity):
    email : str
    first_name : str
    last_name : str
    password : str

