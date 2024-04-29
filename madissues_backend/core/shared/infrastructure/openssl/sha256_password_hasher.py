import hashlib
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher


class SHA256PasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
