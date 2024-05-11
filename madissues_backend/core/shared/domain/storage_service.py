from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def upload_b64_image(self, image: str, folder: str, image_name: str) -> str:
        ...

    @abstractmethod
    def get_b64_image(self, folder: str, image_name: str) -> bytes:
        ...

    @abstractmethod
    def delete_image(self, folder: str, image_name: str):
        ...

    @abstractmethod
    def clear_folder(self, folder: str):
        ...