import io
import tempfile

from rest_framework.test import APITestCase
from rest_framework import status
from stickers.models import Sticker, Groups
from PIL import Image


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


class StickerTestCase(APITestCase):
    url = "/api/sticker"

    def setUp(self):
        Sticker.objects.create(name="Sticker Name", meta="", image=None, group=None)

    def test_get_sticker(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["name"], "Sticker Name")

    def test_post_sticker(self):
        group = Groups.objects.create(name="My New Group")
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            "name": "My sticker name",
            "meta": "{}",
            "image": tmp_file,
            "group": group.id
        }

        response = self.client.post(self.url, data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result['name'], "My sticker name")

    def test_update_sticker(self):
        pk = "1"
        data = {
            "name": "My updated Sticker name",
        }

        response = self.client.patch(self.url + f"/{pk}", data=data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(result['name'], "My updated Sticker name")

    def test_delete_sticker(self):
        pk = "1"

        response_del = self.client.delete(self.url + f"/{pk}")
        response_get = self.client.get(self.url + f"/{pk}")

        self.assertEqual(response_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)
