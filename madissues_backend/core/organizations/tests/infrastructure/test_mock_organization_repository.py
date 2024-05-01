import unittest

from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.mocks.mock_organization_repository import \
    MockOrganizationRepository

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID

#FIXME: this two imports must not be here
from madissues_backend.core.owners.domain.owner_mother import OwnerMother
from madissues_backend.core.owners.infrastructure.mocks.mock_owner_repository import MockOwnerRepository

class TestMockOrganizationRepository(unittest.TestCase):
    def setUp(self):
        # Crear una instancia única de EntityTable
        entity_table = EntityTable()
        self.organization_repository = MockOrganizationRepository(entity_table)
        self.owner_repository = MockOwnerRepository(entity_table)
        self.org1 = OrganizationMother.generate_organization()
        self.org2 = OrganizationMother.generate_organization()
        self.owner1 = OwnerMother.generate_owner()
        self.owner2 = OwnerMother.generate_owner()


    def test_add_organization(self):
        self.organization_repository.add(self.org1)
        self.assertEqual(len(self.organization_repository._organizations), 1)

    def test_get_by_id(self):
        self.organization_repository.add(self.org1)
        retrieved_org = self.organization_repository.get_by_id(self.org1.id)
        self.assertEqual(retrieved_org, self.org1)

    def test_get_by_name(self):
        self.organization_repository.add(self.org1)
        retrieved_org = self.organization_repository.get_by_name(self.org1.name)
        self.assertEqual(retrieved_org, self.org1)

    def test_exists_with_name(self):
        self.organization_repository.add(self.org1)
        self.assertTrue(self.organization_repository.exists_with_name(self.org1.name))
        self.assertFalse(self.organization_repository.exists_with_name(self.org2.name))

    def test_get_by_contact_info(self):
        self.organization_repository.add(self.org1)
        retrieved_org = self.organization_repository.get_by_contact_info(self.org1.contact_info)
        self.assertEqual(retrieved_org, self.org1)

    def test_save_organization(self):
        self.organization_repository.add(self.org1)
        self.org1.name = "NewOrgName"
        self.organization_repository.save(self.org1)
        updated_org = self.organization_repository.get_by_id(self.org1.id)
        self.assertEqual(updated_org.name, "NewOrgName")

    def test_remove_organization(self):
        self.organization_repository.add(self.org1)
        self.organization_repository.remove(self.org1.id)
        self.assertEqual(len(self.organization_repository._organizations), 0)

    def test_get_by_id_nonexistent(self):
        retrieved_org = self.organization_repository.get_by_id(GenericUUID.next_id())
        self.assertIsNone(retrieved_org)

    def test_get_by_name_nonexistent(self):
        retrieved_org = self.organization_repository.get_by_name("Nonexistent")
        self.assertIsNone(retrieved_org)

    def test_get_by_contact_info_nonexistent(self):
        retrieved_org = self.organization_repository.get_by_contact_info("Nonexistent")
        self.assertIsNone(retrieved_org)

    def test_save_nonexistent_organization(self):
        with self.assertRaises(ValueError):
            self.organization_repository.save(self.org1)

    def test_remove_nonexistent_organization(self):
        with self.assertRaises(ValueError):
            self.organization_repository.remove(GenericUUID("nonexistent"))

    def test_change_organization_owner(self):
        """
        Add an organization and owner to the repository, then change the owner of the organization
        and check if the owner of the organization has been updated
        """
        self.organization_repository.add(self.org1)
        self.owner_repository.add(self.owner2)
        updated_org = self.organization_repository.set_owner(self.org1.id, self.owner2.id)
        self.assertEqual(updated_org.owner_id, self.owner2.id)

        owned_organizations = self.owner_repository.get_owned_organizations(self.owner2.id)
        print("Owned organizations: ", owned_organizations)





if __name__ == '__main__':
    unittest.main()
