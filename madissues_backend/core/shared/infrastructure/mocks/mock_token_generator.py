from madissues_backend.core.shared.domain.token_generator import TokenGenerator


class MockTokenGenerator(TokenGenerator):
    def generate(self):
        return 'mock_token'