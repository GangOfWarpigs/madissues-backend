from fastapi.testclient import TestClient

from madissues_backend.apps.rest_api.main import app
from madissues_backend.core.shared.domain.value_objects import GenericUUID

client = TestClient(app)


def test_end_to_end_sign_up_and_login_owner():
    request = {
        "first_name": "Jhon",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "ValidPass123!",
        "verify_password": "ValidPass123!",
        "phone_number": "+34677609928"
    }

    response = client.post("/owners/signup", json=request)

    print(response.json())

    request = {
        "email": "john.doe@example.com",
        "password": "ValidPass123!"
    }

    response = client.post("/owners/signin", json=request)

    owner_token = response.json()["success"]["token"]

    assert owner_token is not None, "Token has been created successfully"

