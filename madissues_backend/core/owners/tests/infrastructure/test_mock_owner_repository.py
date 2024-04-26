import unittest

from madissues_backend.core.owners.domain.owner_mother import OwnerMother
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MyTestCase(unittest.TestCase):
    # Setup
    def setUp(self):
        entity_table = EntityTable()
        self.repository = MockOwnerRepository(entity_table)

    def test_create_owner(self):
        owner_generator = OwnerMother()
        new_owner = owner_generator.generate_owner()
        self.repository.add(new_owner)
        self.assertEqual(len(self.repository.owners), 1)

    def test_remove_owner(self):
        owner_generator = OwnerMother()
        new_owner = owner_generator.generate_owner()
        id = new_owner.id
        self.repository.add(new_owner)
        self.repository.remove(id)
        self.assertEqual(len(self.repository.owners), 0)

    def test_get_owner_by_id(self):
        owner_generator = OwnerMother()
        new_owner = owner_generator.generate_owner()
        id = new_owner.id
        self.repository.add(new_owner)
        owner = self.repository.get_by_id(id)
        print("Added User: ", new_owner)
        print("Retrieved User: ", owner)
        self.assertEqual(owner, new_owner)

    def test_save_owner(self):
        owner_generator = OwnerMother()
        new_owner = owner_generator.generate_owner()
        id = new_owner.id
        self.repository.add(new_owner)
        new_owner.first_name = "New Name"
        self.repository.save(new_owner)
        owner = self.repository.get_by_id(id)
        self.assertEqual(owner.first_name, "New Name")

    def test_owner_already_exists_throw_exception(self):
        try:
            owner_generator = OwnerMother()
            new_owner = owner_generator.generate_owner()
            self.repository.add(new_owner)
            self.repository.add(new_owner)
            assert False, "Adding owner with same ID must throw value error exception"
        except ValueError as e:
            assert str(e) == "Owner already exists", "If owner already exists must throw value error"

    def test_owner_already_exists(self):
        try:
            self.repository.remove(GenericUUID.next_id())
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner does not exists", "If owner already exists must throw value error"

    def test_get_non_existing_owner_by_id(self):
        try:
            self.repository.get_by_id(GenericUUID.next_id())
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner not found", "If owner already exists must throw value error"

    def test_save_non_existing_owner(self):
        try:
            owner_generator = OwnerMother()
            new_owner = owner_generator.generate_owner()
            self.repository.save(new_owner)
            assert False, "Remove owner that does not exist should throw exception"
        except ValueError as e:
            assert str(e) == "Owner not found", "If owner already exists must throw value error"


if __name__ == '__main__':
    unittest.main()
