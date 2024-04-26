import unittest
import random

from madissues_backend.core.owners.tests.object_mothers import OwnerObjectMother
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.owners.infrastructure.mocks.in_memory_owner_repository import InMemoryOwnerRepository


class MyTestCase(unittest.TestCase):
    def test_create_user(self):
        repository = InMemoryOwnerRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        repository.add(new_user)
        self.assertEqual(len(repository.owners), 1)

    def test_remove_user(self):
        repository = InMemoryOwnerRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        repository.remove(id)
        self.assertEqual(len(repository.owners), 0)

    def test_get_user_by_id(self):
        repository = InMemoryOwnerRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        user = repository.get_by_id(id)
        print("Added User: ", new_user)
        print("Retrieved User: ", user)
        self.assertEqual(user, new_user)

    def test_save_user(self):
        repository = InMemoryOwnerRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        new_user.first_name = "New Name"
        repository.save(new_user)
        user = repository.get_by_id(id)
        self.assertEqual(user.first_name, "New Name")

    def test_owner_already_exists_throw_exception(self):
        try:
            repository = InMemoryOwnerRepository()
            user_generator = OwnerObjectMother()
            new_user = user_generator.generate_owner()
            repository.add(new_user)
            repository.add(new_user)
            assert False, "Adding owner with same ID must throw value error exception"
        except ValueError as e:
            assert str(e) == "Owner already exists", "If owner already exists must throw value error"

    def test_owner_already_exists(self):
        try:
            repository = InMemoryOwnerRepository()
            repository.remove(GenericUUID.next_id())
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner does not exists", "If owner already exists must throw value error"
    def test_get_owner_by_id(self):
        try:
            repository = InMemoryOwnerRepository()
            repository.get_by_id(GenericUUID.next_id())
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner not found", "If owner already exists must throw value error"

    def test_save_owner(self):
        try:
            repository = InMemoryOwnerRepository()
            user_generator = OwnerObjectMother()
            new_user = user_generator.generate_owner()
            repository.save(new_user)
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner not found", "If owner already exists must throw value error"

if __name__ == '__main__':
    unittest.main()
