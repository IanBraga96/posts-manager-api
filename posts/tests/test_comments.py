from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


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
