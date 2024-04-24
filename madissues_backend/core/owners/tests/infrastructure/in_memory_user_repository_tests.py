import unittest
import random

from madissues_backend.core.owners.tests.object_mothers import OwnerObjectMother
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.owners.infrastructure.mocks.in_memory_user_repository import InMemoryUserRepository


class MyTestCase(unittest.TestCase):
    def test_create_user(self):
        repository = InMemoryUserRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        repository.add(new_user)
        self.assertEqual(len(repository.users), 1)

    def test_remove_user(self):
        repository = InMemoryUserRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        repository.remove(id)
        self.assertEqual(len(repository.users), 0)

    def test_get_user_by_id(self):
        repository = InMemoryUserRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        user = repository.get_by_id(id)
        print("Added User: ", new_user)
        print("Retrieved User: ", user)
        self.assertEqual(user, new_user)

    def test_save_user(self):
        repository = InMemoryUserRepository()
        user_generator = OwnerObjectMother()
        new_user = user_generator.generate_owner()
        id = new_user.id
        repository.add(new_user)
        new_user.first_name = "New Name"
        repository.save(new_user)
        user = repository.get_by_id(id)
        self.assertEqual(user.first_name, "New Name")

if __name__ == '__main__':
    unittest.main()
