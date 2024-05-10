import os
import requests
from requests import Response

from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerService, TaskManagerFactory

from dotenv import load_dotenv


class TrelloTaskManagerService(TaskManagerService):

    def __init__(self, task_manager_config: TaskManagerConfig):
        self.base_url = "https://api.trello.com/1/"
        self.config = task_manager_config

    def _make_request(self, method: str, endpoint: str, params: dict) -> Response:
        url = self.base_url + endpoint
        params["key"] = self.config.api_key
        params["token"] = self.config.token

        response = requests.request(method, url, params=params)

        if response.status_code != 200:
            self._handle_error_response(response)

        return response

    def _handle_error_response(self, response: Response) -> None:
        raise Exception(f"Trello API Error: {response.status_code} - {response.text}")

    def is_api_key_valid(self) -> bool:
        query = {
            "query": "hello",  # Any query
        }
        response = self._make_request("GET", "search", query)
        print("Response: ", response.json())
        return response.status_code == 200

    def create_organization(self, name: str) -> str:
        query = {
            "displayName": name,
        }
        response = self._make_request("POST", "organizations", query)
        print("Response: ", response.json())
        return str(response.json()["id"])

    def delete_organization(self, organization_id: str):
        response = self._make_request("DELETE", f"organizations/{organization_id}", {})
        return response.json()

    def create_empty_board(self, organization_id: str, name: str) -> str:
        query = {
            "idOrganization": organization_id,
            "name": name,
            "defaultLists": "false"
        }
        response = self._make_request("POST", "boards", query)
        return str(response.json()["id"])

    def get_board_id(self, board_name: str):
        query: dict = {}
        response = self._make_request("GET", f"boards/{board_name}", query)

        # Get the id field from the response
        return response.json()

    def get_boards_in_organization(self, organization_id_or_name: str) -> list[str]:
        query: dict = {}
        response = self._make_request("GET", f"organizations/{organization_id_or_name}/boards", query)
        return response.json()

    def create_empty_list(self, board_id: str, name: str) -> str:
        query = {
            "idBoard": board_id,
            "name": name,
        }
        response = self._make_request("POST", "lists", query)
        return str(response.json()["id"])

    def invite_user(self, organization_id: str, email: str):
        query = {
            "email": email,
            "fullName": email.split("@")[0],
        }
        response = self._make_request("PUT", f"organizations/{organization_id}/members", query)
        return response.json()


class TrelloTaskManagerFactory(TaskManagerFactory):
    def of(self, task_manager_config: TaskManagerConfig) -> TaskManagerService:
        return TrelloTaskManagerService(task_manager_config)


if __name__ == "__main__":
    pass
    # load_dotenv()
    # config = TaskManagerConfig(
    #     service="trello",
    #     api_key=str(os.getenv("TRELLO_API_KEY")),
    #     token=str(os.getenv("TRELLO_TOKEN"))
    # )
    # service = TrelloTaskManagerFactory().of(config)
    # print("Requesting Trello API to check if the key is valid...")
    # result = service.is_api_key_valid()
    # print("Is API Key Valid: ", result)
    #
    # organization_id = service.create_organization("DEII")
    # print("Create Organization: ", organization_id)
    # board_id = service.create_empty_board(organization_id, "Faqs")
    # print("Create Empty Board: ", board_id)
    # list_id = service.create_empty_list(board_id, "Queued")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "In progress")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "Solved")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "Not solved")
    # print("Create Empty List: ", list_id)
    #
    # # -------------------------------------
    # board_id = service.create_empty_board(organization_id, "Issues")
    # print("Create Empty Board: ", board_id)
    # list_id = service.create_empty_list(board_id, "Queued")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "In progress")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "Solved")
    # print("Create Empty List: ", list_id)
    # list_id = service.create_empty_list(board_id, "Not solved")
    # print("Create Empty List: ", list_id)

    # res_inv = service.invite_user(organization_id, "antapagon101@gmail.com")
    # print("Invite User: ", res_inv)

    # result = service.delete_organization("663e92bdadda338704418d23")
    # print("Delete Organization: ", result)

