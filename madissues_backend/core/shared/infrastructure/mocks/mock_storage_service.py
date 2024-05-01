from madissues_backend.core.shared.domain.storage_service import StorageService


class MockStorageService(StorageService):
    def upload_b64_image(self, image: str, path: str = "", final_name="") -> str:
        return "uploaded_was_called.png"