import unittest

from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.owners.domain.owner_mother import OwnerMother


class MyTestCase(unittest.TestCase):
    def test_create_10_owners(self):
        for _ in range(1, 10):  # Can not create more than 10 owners, so that they remain unique
            owner = OwnerMother.generate_owner()
            self.assertIsInstance(owner, Owner)


if __name__ == '__main__':
    unittest.main()
