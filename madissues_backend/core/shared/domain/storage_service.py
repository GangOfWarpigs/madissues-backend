from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def upload_b64_image(self, image: str, path: str = "", final_name="") -> str:
        ...