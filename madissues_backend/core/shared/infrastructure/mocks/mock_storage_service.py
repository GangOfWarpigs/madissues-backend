import base64

from madissues_backend.core.shared.domain.storage_service import StorageService


class MockStorageService(StorageService):
    def upload_b64_image(self, image: str, path: str = "", final_name="") -> str:
        return "uploaded_was_called.png"

    def get_b64_image(self, folder: str, image_name: str) -> bytes:
        return b"get_image_was_called"

    def delete_image(self, folder: str, image_name: str):
        return "delete_image_was_called"
