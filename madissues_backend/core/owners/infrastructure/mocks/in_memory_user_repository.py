from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner


class InMemoryUserRepository(OwnerRepository):
    def get_owner_by_email(self, email: str) -> Owner:
        raise NotImplemented

    users: list[Owner]

    def __init__(self):
        self.users = []

    def add(self, entity: Owner):
        if self.__index_user_by_id(entity.id) is not None:
            raise Exception("User already exists")
        self.users.append(entity)

    def remove(self, user_id: GenericUUID):
        index = self.__index_user_by_id(user_id)
        if index is None:
            raise Exception("User does not exist")
        del self.users[index]

    def get_by_id(self, user_id: GenericUUID) -> Owner:
        index = self.__index_user_by_id(user_id)
        if index is None:
            raise Exception("User not found")
        return self.users[index]

    def save(self, entity: Owner):
        index = self.__index_user_by_id(entity.id)
        if index is None:
            raise Exception("User not found")
        self.users[index] = entity

    def __index_user_by_id(self, user_id) -> int | None:
        for i in range(len(self.users)):
            if self.users[i].id == user_id:
                return i
        return None

    def exists_owner_with_email(self, email: str) -> bool:
        for user in self.users:
            if user.email == email:
                return True
        return False
