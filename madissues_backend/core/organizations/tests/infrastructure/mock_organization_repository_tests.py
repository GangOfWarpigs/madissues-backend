import unittest

from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository
from madissues_backend.core.organizations.tests.common.organization_factory import OrganizationFactory
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestMockOrganizationRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MockOrganizationRepository()
        self.org1 = OrganizationFactory.create_organization()
        self.org2 = OrganizationFactory.create_organization()

    def test_add_organization(self):
        self.repository.add(self.org1)
        self.assertEqual(len(self.repository._organizations), 1)

    def test_get_by_id(self):
        self.repository.add(self.org1)
        retrieved_org = self.repository.get_by_id(self.org1.id)
        self.assertEqual(retrieved_org, self.org1)

    def test_get_by_name(self):
        self.repository.add(self.org1)
        retrieved_org = self.repository.get_by_name(self.org1.name)
        self.assertEqual(retrieved_org, self.org1)

    def test_exists_with_name(self):
        self.repository.add(self.org1)
        self.assertTrue(self.repository.exists_with_name(self.org1.name))
        self.assertFalse(self.repository.exists_with_name(self.org2.name))

    def test_get_by_contact_info(self):
        self.repository.add(self.org1)
        retrieved_org = self.repository.get_by_contact_info(self.org1.contact_info)
        self.assertEqual(retrieved_org, self.org1)

    def test_save_organization(self):
        self.repository.add(self.org1)
        self.org1.name = "NewOrgName"
        self.repository.save(self.org1)
        updated_org = self.repository.get_by_id(self.org1.id)
        self.assertEqual(updated_org.name, "NewOrgName")

    def test_remove_organization(self):
        self.repository.add(self.org1)
        self.repository.remove(self.org1.id)
        self.assertEqual(len(self.repository._organizations), 0)

    def test_get_by_id_nonexistent(self):
        retrieved_org = self.repository.get_by_id(GenericUUID.next_id())
        self.assertIsNone(retrieved_org)

    def test_get_by_name_nonexistent(self):
        retrieved_org = self.repository.get_by_name("Nonexistent")
        self.assertIsNone(retrieved_org)

    def test_get_by_contact_info_nonexistent(self):
        retrieved_org = self.repository.get_by_contact_info("Nonexistent")
        self.assertIsNone(retrieved_org)

    def test_save_nonexistent_organization(self):
        with self.assertRaises(ValueError):
            self.repository.save(self.org1)

    def test_remove_nonexistent_organization(self):
        with self.assertRaises(ValueError):
            self.repository.remove(GenericUUID("nonexistent"))


if __name__ == '__main__':
    unittest.main()
