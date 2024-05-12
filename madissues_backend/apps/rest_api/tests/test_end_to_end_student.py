import unittest

from fastapi.testclient import TestClient

from madissues_backend.apps.rest_api.dependencies import database
from madissues_backend.apps.rest_api.main import app
from madissues_backend.core.shared.domain.value_objects import GenericUUID

client = TestClient(app)


class TestEndToEnd(unittest.TestCase):
    def test_student_organization_endpoints(self):
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
            "year": 3,
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
            "email": "test.email@gmail.com",
            "office_link": "https://www.dis.ulpgc.es/pepe",
            "courses": [course_id]
        }

        response = client.post("/organizations/" + organization_id + "/teachers/", json=teachers, headers={
            "token": owner_token
        })

        teacher_id = response.json()["success"]["id"]

        assert response.json()["success"] is not None, "is succeded"

        degree = {
            "organization_id": organization_id,
            "name": "name of subject"
        }

        response = client.post("/organizations/" + organization_id + "/degrees/", json=degree, headers={
            "token": owner_token
        })

        assert response.json()["success"] is not None, "is succeded"



        query = client.get("/organizations/" + organization_id)

        assert query.json()["error"] is None, "Error must not be setted"
        assert query.json()["success"]["id"] is not None, "Id must not be none"


        query = client.get("/organizations/12")


        assert query.json()["error"]["error_code"] == 0, "Error code must be 0"
        self.assertIn("UUID", query.json()["error"]["error_message"] , "Error code must be 0")


        query = client.get("/organizations/" + organization_id + "/degrees")

        assert query.json()["error"] is None, "Error must not be setted"
        assert len(query.json()["success"]) == 1, "Id must not be none"


        query = client.get("/organizations/12/degrees")


        assert query.json()["error"]["error_code"] == 0, "Error code must be 0"
        self.assertIn("UUID", query.json()["error"]["error_message"] , "Error code must be 0")

        query = client.get("/organizations/" + organization_id + "/teachers")

        assert query.json()["error"] is None, "Error must not be setted"
        assert len(query.json()["success"]) == 1, "Id must not be none"


        query = client.get("/organizations/12/teachers")


        assert query.json()["error"]["error_code"] == 0, "Error code must be 0"
        self.assertIn("UUID", query.json()["error"]["error_message"] , "Error code must be 0")


        student = {
            "organization_id": organization_id,
            "email": "test.email@test.com",
            "first_name": "Test",
            "last_name": "Test",
            "password": "ValidPassword123!",
            "verify_password": "ValidPassword123!",
            "phone_number": "123123123",
            "degreeId": "12",
            "started_studies_date": "1999-01-01"
        }


        query = client.post("/students/signup", json=student)

        assert query.json()["error"]["error_code"] == 0, "Error code must be 0"
        self.assertIn("UUID", query.json()["error"]["error_message"] , "Error code must be 0")

        student = {
            "organization_id": organization_id,
            "email": "test.email@test.com",
            "first_name": "Test",
            "last_name": "Test",
            "password": "ValidPassword123!",
            "verify_password": "ValidPassword123!",
            "phone_number": "123123123",
            "degreeId": organization_id,
            "started_studies_date": "1999-01-01"
        }


        query = client.post("/students/signup", json=student)

        assert query.json()["error"] is None, "Not error here my boyz"

        student_token = query.json()["success"]["token"]

        assert student_token is not None, "Student token is not none"

        issue = {
            "title": "string",
            "description": "string",
            "details": "string",
            "proofs": [
            ],
            "course": course_id,
            "teachers": [
                teacher_id
            ],
            "organization_id": organization_id
        }

        query = client.post("/issues", json=issue, headers={
            "token": student_token
        })

        assert query.json()["error"] is None, "Not error here my boyz"

        print(query.json()["success"]["id"])

        query = client.get("organizations/" + organization_id + "/issues", headers={
                           "token": owner_token
        })


        assert query.json()["error"] is None, "Not error here my boyz"
        assert len(query.json()["success"]) == 1, "Just the two of us"
        #check that student field is there and with name and year of student created
        assert query.json()["success"][0]["student"]["name"] == "Test Test", "Just the two of us"
        assert query.json()["success"][0]["student"]["year"] == "1999", "Stand by me"
        #check that the teacher is the name of the teacher
        assert query.json()["success"][0]["teachers"][0] == "string string", "Hound dog"
        #check that the name of the course is the same as the course created
        assert query.json()["success"][0]["course"] == "string", "What a wonderful world"

        #TEST CASES MUST EXCEPT WITH NAMES OF SONGS FROM 60s, 80s and 70s

        #check studet me
        query = client.get("students/me", headers={
                           "token": student_token
        })

        assert query.json()["error"] is None, "Not error here my boyz"
        assert query.json()["success"]["first_name"] == "Test", "Just the two of us"
        assert query.json()["success"]["last_name"] == "Test", "Just the two of us"

        print(query.json())


