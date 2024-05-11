import base64
import os
import unittest
from madissues_backend.core.shared.infrastructure.storage.local_storage_service import LocalStorageService


class TestLocalStorageService(unittest.TestCase):

    def setUp(self):
        # Construir la ruta al directorio base de los tests
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.storage_service = LocalStorageService(os.path.join(self.base_path, "../../../../../media"))

    def test_upload_b64_image(self):
        test_b64image_path = os.path.join(self.base_path, "cat.b64")
        with open(test_b64image_path, "rb") as file:
            image = file.read().decode("utf-8")
            path = self.storage_service.upload_b64_image(image, folder="tests", image_name="cat")
            self.assertEqual(path, "cat.png")

    def test_get_b64_image(self):
        test_b64image_path = os.path.join(self.base_path, "cat.b64")
        with open(test_b64image_path, "rb") as file:
            image = file.read().decode("utf-8")
            path = self.storage_service.upload_b64_image(image, folder="tests", image_name="cat")

        retrieved_image = self.storage_service.get_b64_image(image_name="cat", folder="tests")
        encoded_retrieved_image = base64.b64encode(retrieved_image).decode("utf-8")
        self.assertEqual(image, encoded_retrieved_image)

    def test_delete_image(self):
        test_b64image_path = os.path.join(self.base_path, "cat.b64")
        with open(test_b64image_path, "rb") as file:
            image = file.read().decode("utf-8")
            path = self.storage_service.upload_b64_image(image, folder="tests", image_name="cat")

        self.storage_service.delete_image(folder="tests", image_name="cat")
        with self.assertRaises(FileNotFoundError):
            self.storage_service.delete_image(folder="tests", image_name="cat")

    def test_clear_folder(self):
        test_b64image_path = os.path.join(self.base_path, "cat.b64")
        with open(test_b64image_path, "rb") as file:
            image = file.read().decode("utf-8")
            path = self.storage_service.upload_b64_image(image, folder="tests", image_name="cat")

        self.storage_service.clear_folder(folder="tests")
        with self.assertRaises(FileNotFoundError):
            self.storage_service.get_b64_image(image_name="cat", folder="tests")


if __name__ == '__main__':
    unittest.main()
