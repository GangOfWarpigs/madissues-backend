import base64
import unittest

from madissues_backend.core.shared.infrastructure.local_storage_service import LocalStorageService


class TestLocalStorageService(unittest.TestCase):

    def setUp(self):
        self.storage_service = LocalStorageService(media_path='../../../../media/')

    def test_upload_b64_image(self):
        test_b64image_path = "./cat.b64"
        with open(test_b64image_path, "rb") as file:
            image = file.read().decode("utf-8")
            path = self.storage_service.upload_b64_image(image, path="tests/", final_name="cat.jpeg")
            self.assertEqual(path, "../../../../media/tests/cat.jpeg")


if __name__ == '__main__':
    unittest.main()
