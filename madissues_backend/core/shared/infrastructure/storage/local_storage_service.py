import base64
import os

from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class LocalStorageService(StorageService):
    def __init__(self, media_path: str):
        self.media_path: str = media_path

    def upload_b64_image(self, image: str, folder: str, image_name: str) -> str:
        """Receives image in base64 format and returns the path where it was saved"""

        if (folder == "") or (image_name == ""):
            raise ValueError("Folder and image_name cannot be empty")

        # Decode the image
        image=image.split(",")[1]
        image_data = base64.b64decode(image)

        # Save the image in media folder
        full_path = f"{self.media_path}/{folder}/{image_name}"

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as file:
            file.write(image_data)

        if image_name is None:
            image_name = str(GenericUUID.next_id())

        return str(full_path)

    def get_b64_image(self, folder: str, image_name: str) -> bytes:
        """Returns the image in bytes"""
        if (folder == "") or (image_name == ""):
            raise ValueError("Folder and image_name cannot be empty")

        full_path = f"{self.media_path}/{folder}/{image_name}"
        print(full_path)

        if os.path.exists(full_path):
            with open(full_path, "rb") as file:
                return file.read()
        else:
            raise FileNotFoundError(f"Image {image_name} not found")

    def delete_image(self,  folder: str, image_name: str):
        """Deletes an image from the media folder"""
        if (folder == "") or (image_name == ""):
            raise ValueError("Folder and image_name cannot be empty")

        if image_name == "":
            raise ValueError("Image name cannot be empty")

        # Save the image in media folder
        full_path = f"{self.media_path}/{folder}/{image_name}"

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image {image_name} not found")

        os.remove(full_path)
