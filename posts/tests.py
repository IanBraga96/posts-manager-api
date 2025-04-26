from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mock_post_data = {
            "username": "testuser",
            "title": "Test Title",
            "content": "Test Content",
        }
        self.mock_response_data = {
            "id": 1,
            "username": "testuser",
            "title": "Test Title",
            "content": "Test Content",
            "created_datetime": "2023-08-10T12:00:00Z",
        }
        print("\n=== Starting new test ===")

    @patch("posts.views.requests.get")
    def test_get_posts_list(self, mock_get):
        print("\nTesting posts listing...")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [self.mock_response_data]}
        mock_get.return_value = mock_response

        url = reverse("post-list-create")
        response = self.client.get(url)

        print(f"Received status code: {response.status_code}")
        print(f"Received data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_get.assert_called_once_with("https://dev.codeleap.co.uk/careers/")