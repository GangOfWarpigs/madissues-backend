from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner


class InMemoryOwnerRepository(OwnerRepository):
    owners: list[Owner]

    def __init__(self):
        self.owners = []

    def __index_owner_by_id(self, user_id) -> int | None:
        for i in range(len(self.owners)):
            if self.owners[i].id == user_id:
                return i
        return None

    def add(self, entity: Owner):
        if self.__index_owner_by_id(entity.id) is not None:
            raise Exception("Owner already exists")
        self.owners.append(entity)

    def remove(self, user_id: GenericUUID):
        index = self.__index_owner_by_id(user_id)
        if index is None:
            raise Exception("Owner does not exist")
        del self.owners[index]

    def get_by_id(self, user_id: GenericUUID) -> Owner:
        index = self.__index_owner_by_id(user_id)
        if index is None:
            raise Exception("Owner not found")
        return self.owners[index]

    def save(self, entity: Owner):
        index = self.__index_owner_by_id(entity.id)
        if index is None:
            raise Exception("Owner not found")
        self.owners[index] = entity



    def exists_owner_with_email(self, email: str) -> bool:
        for user in self.owners:
            if user.email == email:
                return True
        return False
