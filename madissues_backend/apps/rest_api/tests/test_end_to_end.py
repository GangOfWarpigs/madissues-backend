import unittest

from fastapi.testclient import TestClient

from madissues_backend.apps.rest_api.main import app
from madissues_backend.core.shared.domain.value_objects import GenericUUID

client = TestClient(app)


class TestEndToEnd(unittest.TestCase):
    def test_end_to_end_sign_up_and_login_owner(self):
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

    def test_organizations_endpoints(self):
        request = {
            "first_name": "Jhon",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "ValidPass123!",
            "verify_password": "ValidPass123!",
            "phone_number": "+34677609928"
        }

        response = client.post("/owners/signup", json=request)

        request = {
            "email": "john.doe@example.com",
            "password": "ValidPass123!"
        }

        response = client.post("/owners/signin", json=request)

        assert response.json()["error"] is None, "There are no errors"

        owner_token = response.json()["success"]["token"]

        assert owner_token is not None, "Token has been created successfully"

        organization = {
            "name": "test",
            "logo": "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            "description": "test",
            "contact_info": "test",
            "primary_color": "#f5f5f5",
            "secondary_color": "#f5f5f5"
        }

        response = client.post("/organizations/", json=organization, headers={
            "token": owner_token
        })

        organization_id = response.json()["success"]["id"]

        assert organization_id is not None, "Organization has been created successfully"
        assert response.json()["error"] is None, "There are no errors"

        course = {
            "organization_id": organization_id,
            "name": "string",
            "code": "string",
            "year": 4,
            "icon": "string",
            "primary_color": "#f5f5f5",
            "secondary_color": "#f5f5f5"
        }

        response = client.post("/organizations/" + organization_id + "/courses/", json=course, headers={
            "token": owner_token
        })

        course_id = response.json()["success"]["id"]

        assert course_id is not None, "Token has been created successfully"

        response = client.get("/organizations/" + organization_id + "/courses", headers={
            "token": owner_token
        })

        assert response.json()["success"][0]["id"] is not None, "Is allright mamma, its allright to me"

        teachers = {
            "organization_id": organization_id,
            "first_name": "string",
            "last_name": "string",
            "email": "jrpenasco@gmail.com",
            "office_link": "https://www.dis.ulpgc.es/pepe",
            "courses": [course_id]
        }

        response = client.post("/organizations/" + organization_id + "/teachers/", json=teachers, headers={
            "token": owner_token
        })

        assert response.json()["success"] is not None, "is succeded"

        degree = {
          "organization_id": organization_id,
          "name": "name of subject"
        }

        response = client.post("/organizations/" + organization_id + "/degrees/", json=degree, headers={
            "token": owner_token
        })
        print(response.json())
        assert response.json()["success"] is not None, "is succeded"

    def test_organization_endpoints(self):
        request = {
            "first_name": "Jhon",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "ValidPass123!",
            "verify_password": "ValidPass123!",
            "phone_number": "+34677609928"
        }

        response = client.post("/owners/signup", json=request)

        request = {
            "email": "john.doe@example.com",
            "password": "ValidPass123!"
        }

        response = client.post("/owners/signin", json=request)

        assert response.json()["error"] is None, "There are no errors"

        owner_token = response.json()["success"]["token"]

        assert owner_token is not None, "Token has been created successfully"

        organization = {
            "name": "test",
            "logo": "iVBORw0KGgoAAAANSUhEUgAAAoMAAAHiCAYAAACTLsbsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUA",
            "description": "test",
            "contact_info": "test",
            "primary_color": "#f5f5f5",
            "secondary_color": "#f5f5f5"
        }

        response = client.post("/organizations/", json=organization, headers={
            "token": owner_token
        })

        organization_id = response.json()["success"]["id"]

        assert organization_id is not None, "Organization has been created successfully"
        assert response.json()["error"] is None, "There are no errors"

        course = {
            "organization_id": organization_id,
            "name": "string",
            "code": "string",
            "year": 2,
            "icon": "string",
            "primary_color": "#f5f5f5",
            "secondary_color": "#f5f5f5"
        }

        response = client.post("/organizations/" + organization_id + "/courses/", json=course, headers={
            "token": owner_token
        })

        course_id = response.json()["success"]["id"]

        assert course_id is not None, "Token has been created successfully"

        response = client.get("/organizations/" + organization_id + "/courses", headers={
            "token": owner_token
        })

        assert response.json()["success"][0]["id"] is not None, "Is allright mamma, its allright to me"

        teachers = {
            "organization_id": organization_id,
            "first_name": "string",
            "last_name": "string",
            "email": "jrpenasco@gmail.com",
            "office_link": "https://www.dis.ulpgc.es/pepe",
            "courses": [course_id]
        }

        response = client.post("/organizations/" + organization_id + "/teachers/", json=teachers, headers={
            "token": owner_token
        })

        assert response.json()["success"] is not None, "is succeded"

        degree = {
            "organization_id": organization_id,
            "name": "name of subject"
        }

        response = client.post("/organizations/" + organization_id + "/degrees/", json=degree, headers={
            "token": owner_token
        })
        print(response.json())
        assert response.json()["success"] is not None, "is succeded"
