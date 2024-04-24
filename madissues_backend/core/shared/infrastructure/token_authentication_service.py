from madissues_backend.core.shared.application.authentication_service import AuthenticationService


class TokenAuthenticationService(AuthenticationService):
    def __init__(self, token):
        self.token = token

    def is_authenticated(self):
        return True

    def get_user_id(self) -> int:
        raise NotImplementedError()

    def is_student(self) -> bool:
        raise NotImplementedError()

    def is_site_admin(self) -> bool:
        raise NotImplementedError()

    def is_council_member(self) -> bool:
        raise NotImplementedError()

    def is_owner(self) -> bool:
        raise NotImplementedError()
