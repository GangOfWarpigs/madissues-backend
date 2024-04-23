from madissues_backend.core.shared.domain.password_hasher import PasswordHasher


class MockPasswordHasher(PasswordHasher):
    def hash(self, password):
        return "hashed-password"