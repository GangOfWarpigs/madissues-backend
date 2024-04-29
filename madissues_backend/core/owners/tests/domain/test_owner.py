import unittest

from pydantic import ValidationError

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.infrastructure.mocks.mock_password_hasher import MockPasswordHasher
from madissues_backend.core.shared.infrastructure.mocks.mock_token_generator import MockTokenGenerator


class OwnerTests(unittest.TestCase):
    def setUp(self):
        self.valid_owner_data = {
            'id': GenericUUID.next_id(),
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '123456789',
            'password': 'TestPassword123',
        }

    def test_valid_owner(self):
        owner = Owner(**self.valid_owner_data)
        self.assertIsInstance(owner, Owner)

    def test_invalid_email(self):
        invalid_data = self.valid_owner_data.copy()
        invalid_data['email'] = 'invalid_email.com'
        with self.assertRaises(ValidationError):
            Owner(**invalid_data)

    def test_empty_first_name(self):
        invalid_data = self.valid_owner_data.copy()
        invalid_data['first_name'] = ''
        with self.assertRaises(ValidationError):
            Owner(**invalid_data)

    def test_empty_last_name(self):
        invalid_data = self.valid_owner_data.copy()
        invalid_data['last_name'] = ''
        with self.assertRaises(ValidationError):
            Owner(**invalid_data)

    def test_empty_phone_number(self):
        invalid_data = self.valid_owner_data.copy()
        invalid_data['phone_number'] = ''
        with self.assertRaises(ValidationError):
            Owner(**invalid_data)

    def test_invalid_phone_number_format(self):
        invalid_data = self.valid_owner_data.copy()
        invalid_data['phone_number'] = '123'
        with self.assertRaises(ValidationError):
            Owner(**invalid_data)

    def test_generate_auth_token(self):
        owner = Owner(**self.valid_owner_data)
        token_generator = MockTokenGenerator()
        owner.generate_auth_token(token_generator)
        self.assertNotEqual(owner.token, '')

    def test_password_is_hashed_when_set_password_is_used(self):
        user = Owner(**self.valid_owner_data)
        user.set_password("Contrasena112233*", MockPasswordHasher())
        assert user.password == "hashed-password"

    def test_password_is_secure_always(self):
        try:
            user = Owner(**self.valid_owner_data)
            user.set_password("Pepe", MockPasswordHasher())
            assert False, "Password is not secure and has been pass"
        except ValueError as e:
            assert True, "Password is not secure and has not pass"


if __name__ == '__main__':
    unittest.main()
