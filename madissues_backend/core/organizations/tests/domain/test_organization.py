import unittest
from pydantic import ValidationError

from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class TestOrganization(unittest.TestCase):
    def setUp(self):
        self.valid_organization_data = {
            'id': GenericUUID.next_id(),
            'owner_id': GenericUUID.next_id(),
            'name': 'Test Organization',
            'logo': 'https://example.com/logo.png',
            'description': 'Test description',
            'contact_info': 'test@example.com',
            'primary_color': '#ff0000',
            'secondary_color': '#00ff00',
            'banner': 'https://example.com/banner.jpg',
            'trello_id': GenericUUID.next_id(),
        }

    def test_valid_organization(self):
        organization = Organization(**self.valid_organization_data)
        self.assertIsInstance(organization, Organization)

    def test_invalid_name_min_length(self):
        invalid_organization_data = self.valid_organization_data.copy()
        invalid_organization_data['name'] = ''
        with self.assertRaises(ValidationError):
            Organization(**invalid_organization_data)

    def test_invalid_logo_format(self):
        invalid_organization_data = self.valid_organization_data.copy()
        invalid_organization_data['logo'] = 'not_an_url'
        with self.assertRaises(ValidationError):
            Organization(**invalid_organization_data)

    def test_invalid_description_max_length(self):
        invalid_organization_data = self.valid_organization_data.copy()
        invalid_organization_data['description'] = 'A' * 281
        with self.assertRaises(ValidationError):
            Organization(**invalid_organization_data)

    def test_invalid_contact_info_min_length(self):
        invalid_organization_data = self.valid_organization_data.copy()
        invalid_organization_data['contact_info'] = ''
        with self.assertRaises(ValidationError):
            Organization(**invalid_organization_data)

    def test_invalid_primary_color_format(self):
        invalid_organization_data = self.valid_organization_data.copy()
        invalid_organization_data['primary_color'] = '#invalid'
        with self.assertRaises(ValidationError):
            Organization(**invalid_organization_data)


if __name__ == '__main__':
    unittest.main()
