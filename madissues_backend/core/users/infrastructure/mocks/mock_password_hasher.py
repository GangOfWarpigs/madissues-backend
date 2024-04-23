from madissues_backend.core.users.domain.user.password_hasher import PasswordHasher


class MockPasswordHasher(PasswordHasher):
    def hash(self, password):
        return "hashed-password"