import unittest

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.infrastructure.mock_password_hasher import MockPasswordHasher


class UserTests(unittest.TestCase):
    def test_cannot_instantiate_a_user_with_invalid_email(self):
        try:
            Owner(
                id=GenericUUID.next_id(),
                email="emailnovalido",
                first_name="jose",
                last_name="pepe",
                phone_number="1234"
            )
            assert False
        except ValueError as e:
            assert True

    def test_cannot_instantiate_a_user_with_invalid_uuid(self):
        try:
            Owner(
                id="1234",
                email="emailnovalido",
                first_name="jose",
                last_name="pepe",
                phone_number="1234"
            )
            assert False
        except ValueError as e:
            assert True

    def test_password_is_hashed_when_set_password_is_used(self):
        user = Owner(
            id=GenericUUID.next_id(),
            email="emailnovalido@gmail.com",
            first_name="jose",
            last_name="pepe",
            phone_number="1234"
        )
        user.set_password("Contrasena112233*", MockPasswordHasher())
        assert user.password == "hashed-password"

    def test_password_is_secure_always(self):
        try:
            user = Owner(
                id=GenericUUID.next_id(),
                email="emailnovalido@gmail.com",
                first_name="jose",
                last_name="pepe",
                phone_number="1234"
            )
            user.set_password("Pepe", MockPasswordHasher())
            assert  False, "Password is not secure and has been pass"
        except ValueError as e:
            assert True, "Password is not secure and has not pass"

    def test_cannot_create_user_with_empty_name(self):
        try:
            user = Owner(
                id=GenericUUID.next_id(),
                email="emailnovalido@gmail.com",
                first_name="",
                last_name="pepe",
                phone_number="1234"
            )
            user.set_password("ContrasenaSegura221133*", MockPasswordHasher())
            assert  False, "First name length must be greater than 0"
        except ValueError as e:
            assert True

    def test_cannot_create_user_with_empty_last_name(self):
        try:
            user = Owner(
                id=GenericUUID.next_id(),
                email="emailnovalido@gmail.com",
                first_name="pepe",
                last_name="",
                phone_number="1234"
            )
            user.set_password("ContrasenaSegura221133*", MockPasswordHasher())
            assert  False, "Last name length must be greater than 0"
        except ValueError as e:
            assert True


if __name__ == '__main__':
    unittest.main()
