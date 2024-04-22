import unittest
import random

from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.users.domain.user import User
from madissues_backend.core.users.infrastructure.in_memory_user_repository import InMemoryUserRepository


class RandomUserGenerator:
    # Listas de nombres y apellidos
    names = ["Antonio", "Carlos", "Juan", "Luis", "Pedro", "Pablo", "Miguel", "Francisco", "Jose", "Manuel"]
    last_names = ["Garcia", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Gonzalez", "Rodriguez", "Hernandez",
                  "Diaz"]

    def generate_user(self) -> User:
        name = self.names.pop(random.randint(0, len(self.names) - 1))
        last_name = self.last_names.pop(random.randint(0, len(self.names) - 1))
        return User(
            id=GenericUUID.next_id(),
            email=f"{name}_{last_name}@email.com",
            first_name=name,
            last_name=last_name,
            password="".join(str(random.randint(0, 1000)) for _ in range(6))
        )


class MyTestCase(unittest.TestCase):
    def test_create_user(self):
        repository = InMemoryUserRepository()
        user_generator = RandomUserGenerator()
        new_user = user_generator.generate_user()
        repository.add(new_user)
        self.assertEqual(len(repository.users), 1)

    def test_remove_user(self):
        repository = InMemoryUserRepository()
        user_generator = RandomUserGenerator()
        new_user = user_generator.generate_user()
        id = new_user.id
        repository.add(new_user)
        repository.remove(id)
        self.assertEqual(len(repository.users), 0)

    def test_get_user_by_id(self):
        repository = InMemoryUserRepository()
        user_generator = RandomUserGenerator()
        new_user = user_generator.generate_user()
        id = new_user.id
        repository.add(new_user)
        user = repository.get_by_id(id)
        print("Added User: ", new_user)
        print("Retrieved User: ", user)
        self.assertEqual(user, new_user)

    def test_save_user(self):
        repository = InMemoryUserRepository()
        user_generator = RandomUserGenerator()
        new_user = user_generator.generate_user()
        id = new_user.id
        repository.add(new_user)
        new_user.first_name = "New Name"
        repository.save(new_user)
        user = repository.get_by_id(id)
        self.assertEqual(user.first_name, "New Name")


if __name__ == '__main__':
    unittest.main()
