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

    @patch("posts.views.requests.post")
    def test_create_post(self, mock_post):
        print("\nTesting post creation...")
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = self.mock_response_data
        mock_post.return_value = mock_response

        url = reverse("post-list-create")
        print(f"Sent data: {self.mock_post_data}")
        response = self.client.post(url, self.mock_post_data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_post.assert_called_once_with(
            "https://dev.codeleap.co.uk/careers/", json=self.mock_post_data
        )

    @patch("posts.views.requests.patch")
    def test_update_post(self, mock_patch):
        print("\nTesting post update...")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_response.content = True
        mock_patch.return_value = mock_response

        update_data = {"title": "Updated Title", "content": "Updated Content"}
        url = reverse("post-detail", kwargs={"pk": 1})
        print(f"Update data: {update_data}")
        response = self.client.patch(url, update_data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_patch.assert_called_once_with(
            "https://dev.codeleap.co.uk/careers/1/", json=update_data
        )

    @patch("posts.views.requests.delete")
    def test_delete_post(self, mock_delete):
        print("\nTesting post deletion...")
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        url = reverse("post-detail", kwargs={"pk": 1})
        response = self.client.delete(url)

        print(f"Received status code: {response.status_code}")
        mock_delete.assert_called_once_with("https://dev.codeleap.co.uk/careers/1/")


class PostLikeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_id = 1
        self.username = "testuser"
        print("\n=== Starting new like test ===")

    def test_create_like(self):
        print("\nTesting like creation...")
        url = reverse("post-like", kwargs={"pk": self.post_id})
        data = {"username": self.username}
        response = self.client.post(url, data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["post_id"], self.post_id)

    def test_remove_like(self):
        print("\nTesting like removal...")
        url = reverse("post-like", kwargs={"pk": self.post_id})
        data = {"username": self.username}
        self.client.post(url, data, format="json")

        response = self.client.post(url, data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Like removed")


class PostCommentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_id = 1
        self.username = "testuser"
        self.comment_data = {
            "username": self.username,
            "content": "Test comment with @mention",
        }
        print("\n=== Starting new comment test ===")

    def test_create_comment(self):
        print("\nTesting comment creation...")
        url = reverse("post-comments", kwargs={"pk": self.post_id})
        response = self.client.post(url, self.comment_data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["content"], self.comment_data["content"])
        self.assertEqual(response.data["post_id"], self.post_id)
        self.assertEqual(response.data["mentioned_users"], ["mention"])

    def test_list_comments(self):
        print("\nTesting comments listing...")
        url = reverse("post-comments", kwargs={"pk": self.post_id})
        self.client.post(url, self.comment_data, format="json")

        response = self.client.get(url)

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_comment(self):
        print("\nTesting comment update...")
        url = reverse("post-comments", kwargs={"pk": self.post_id})
        create_response = self.client.post(url, self.comment_data, format="json")
        comment_id = create_response.data["id"]

        update_data = {
            "comment_id": comment_id,
            "username": self.username,
            "content": "Updated comment with @newmention",
        }
        response = self.client.patch(url, update_data, format="json")

        print(f"Received status code: {response.status_code}")
        print(f"Received response: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], update_data["content"])
        self.assertEqual(response.data["mentioned_users"], ["newmention"])

    def test_delete_comment(self):
        print("\nTesting comment deletion...")
        url = reverse("post-comments", kwargs={"pk": self.post_id})
        create_response = self.client.post(url, self.comment_data, format="json")
        comment_id = create_response.data["id"]

        delete_data = {"comment_id": comment_id, "username": self.username}
        response = self.client.delete(url, delete_data, format="json")

        print(f"Received status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_comment_unauthorized(self):
        print("\nTesting unauthorized comment update...")
        url = reverse("post-comments", kwargs={"pk": self.post_id})
        create_response = self.client.post(url, self.comment_data, format="json")
        comment_id = create_response.data["id"]

        update_data = {
            "comment_id": comment_id,
            "username": "different_user",
            "content": "This update should fail",
        }
        response = self.client.patch(url, update_data, format="json")

        print(f"Received status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
