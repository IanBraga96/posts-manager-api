from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


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
