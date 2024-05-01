import base64
import os
from madissues_backend.core.shared.domain.storage_service import StorageService


class LocalStorageService(StorageService):
    def __init__(self, media_path: str):
        self.media_path = media_path

    def upload_b64_image(self, image: str, path: str = "", final_name="") -> str:
        """Receives image in base64 format and returns the path where it was saved"""
        # Decode the image
        image_data = base64.b64decode(image)

        # Save the image in media folder
        path = self.media_path + path

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path + final_name, "wb") as file:
            file.write(image_data)

        return str(path + final_name)

