import uuid
from madissues_backend.core.shared.domain.token_generator import TokenGenerator


class UUIDTokenGenerator(TokenGenerator):
    def generate(self) -> str:
        return str(uuid.uuid4())
