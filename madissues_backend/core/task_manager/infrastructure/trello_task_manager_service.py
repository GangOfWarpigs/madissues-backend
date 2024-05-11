import os
from datetime import datetime
from typing import Any

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
        params["token"] = self.config.api_token

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

    def get_organization(self, organization_id_or_name: str) -> Any:
        query: dict = {}
        response = self._make_request("GET", f"organizations/{organization_id_or_name}", query)
        return response.json()

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
        return [str(board["id"]) for board in response.json()]

    def get_board_by_name_in_organization(self, organization_id_or_name: str, board_name: str) -> str | None:
        query: dict = {}
        response = self._make_request("GET", f"organizations/{organization_id_or_name}/boards", query)
        for board in response.json():
            # Compare both in lowercase
            if board["name"].lower() == board_name.lower():
                return str(board["id"])
        return None

    def create_empty_list(self, board_id: str, name: str) -> str:
        query = {
            "idBoard": board_id,
            "name": name,
        }
        response = self._make_request("POST", "lists", query)
        return str(response.json()["id"])

    def get_board_lists(self, board_id: str) -> list[str]:
        query: dict = {}
        response = self._make_request("GET", f"boards/{board_id}/lists", query)
        return [str(list["id"]) for list in response.json()]

    def get_board_list_by_name(self, board_id: str, list_name: str) -> str | None:
        query: dict = {}
        response = self._make_request("GET", f"boards/{board_id}/lists", query)
        for trello_list in response.json():
            # Compare both in lowercase
            if trello_list["name"].lower() == list_name.lower():
                return str(trello_list["id"])
        return None

    def get_list_cards(self, list_id: str) -> list[str]:
        query: dict = {}
        response = self._make_request("GET", f"lists/{list_id}/cards", query)
        return [str(card["id"]) for card in response.json()]

    def invite_user(self, organization_id: str, email: str):
        query = {
            "email": email,
            "fullName": email.split("@")[0],
        }
        response = self._make_request("PUT", f"organizations/{organization_id}/members", query)
        return response.json()

    def create_card(self, list_id: str, name: str, description: str) -> str:
        query = {
            "idList": list_id,
            "name": name,
            "start": datetime.now().isoformat(),
            "desc": description,
        }
        response = self._make_request("POST", "cards", query)
        return str(response.json()["id"])

    def get_card(self, card_id: str) -> str:
        query: dict = {}
        response = self._make_request("GET", f"cards/{card_id}", query)
        return response.json()

    def update_card(self, card_id: str, name: str, description: str) -> str:
        query = {
            "name": name,
            "desc": description
        }
        response = self._make_request("PUT", f"cards/{card_id}", query)
        return str(response.json()["id"])


class TrelloTaskManagerFactory(TaskManagerFactory):
    def of(self, task_manager_config: TaskManagerConfig) -> TaskManagerService:
        return TrelloTaskManagerService(task_manager_config)


if __name__ == "__main__":
    pass
    load_dotenv()
    config = TaskManagerConfig(
        service="trello",
        api_key=str(os.getenv("TRELLO_API_KEY")),
        api_token=str(os.getenv("TRELLO_TOKEN"))
    )
    service = TrelloTaskManagerFactory().of(config)
    print("Requesting Trello API to check if the key is valid...")
    result = service.is_api_key_valid()
    print("Is API Key Valid: ", result)

    organization_id = service.get_organization("deii6")["id"]
    print("Organization: ", organization_id)

    boards = service.get_boards_in_organization(organization_id)
    print("Boards: ", boards)

    board_id = service.get_board_by_name_in_organization(organization_id, "Faqs")
    print("Board: ", board_id)

    list_id = service.get_board_list_by_name(board_id, "Queued")
    print("List: ", list_id)

    cards = service.get_list_cards(list_id)
    print("Cards: ", cards)

    card_creation = service.create_card(list_id, "Test Card", "This is a test card")
    print("Create Card: ", card_creation)

    cards = service.get_list_cards(list_id)
    print("Updated Cards: ", cards)


    # ------------------------------------
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
