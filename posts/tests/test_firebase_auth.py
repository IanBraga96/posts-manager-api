from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock


class FirebaseAuthenticationTest(TestCase):
    databases = {"default"}

    def setUp(self):
        self.client = APIClient()
        self.like_url = reverse("post-like", kwargs={"pk": 1})
        self.valid_token = "valid-token"
        self.invalid_token = "invalid-token"

    @patch("firebase_admin.auth.verify_id_token")
    def test_request_without_token(self, mock_verify_token):
        response = self.client.post(self.like_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "No token provided")
        mock_verify_token.assert_not_called()

    @patch("firebase_admin.auth.verify_id_token")
    def test_request_with_invalid_token(self, mock_verify_token):
        mock_verify_token.side_effect = Exception("Invalid token")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.invalid_token}")
        response = self.client.post(self.like_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid or expired token")
        mock_verify_token.assert_called_once_with(self.invalid_token)

    @patch("firebase_admin.auth.verify_id_token")
    @patch("firebase_admin.auth.get_user")
    def test_request_with_valid_token(self, mock_get_user, mock_verify_token):
        mock_verify_token.return_value = {"uid": "test_user_id"}

        mock_user = MagicMock()
        mock_user.uid = "test_user_id"
        mock_get_user.return_value = mock_user

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.valid_token}")
        response = self.client.post(self.like_url)

        mock_verify_token.assert_called_once_with(self.valid_token)

        mock_get_user.assert_called_once_with("test_user_id")

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
