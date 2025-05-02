from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from firebase_admin import auth


class AuthAPITest(TestCase):
    databases = {'default'}
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        self.register_data = {
            "name": "TestUser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        self.login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        self.firebase_user_mock = {
            "uid": "test123",
            "name": "TestUser",
            "email": "test@example.com",
            "token": "mock-firebase-token"
        }
        
        print("\n=== Starting Auth Tests ===")
        
        self.patcher = patch('firebase_admin.db.reference')
        self.mock_db = self.patcher.start()
        
    def tearDown(self):
        self.patcher.stop()

    @patch('posts.models.user.User.create')
    @patch('firebase_admin.auth.create_custom_token')
    def test_register_success(self, mock_create_token, mock_create_user):
        print("\nTesting user registration...")
        
        mock_user = MagicMock()
        mock_user.uid = "test123"
        mock_user.name = self.register_data["name"]
        mock_user.email = self.register_data["email"]
        mock_create_user.return_value = mock_user
        
        mock_create_token.return_value = b"mock-firebase-token"
        
        response = self.client.post(
            self.register_url,
            self.register_data,
            format='json'
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.register_data["name"])
        self.assertEqual(response.data["email"], self.register_data["email"])
        self.assertIn("token", response.data)
        
        mock_create_user.assert_called_once_with(
            name=self.register_data["name"],
            email=self.register_data["email"],
            password=self.register_data["password"]
        )

    def test_register_invalid_data(self):
        print("\nTesting invalid registration...")
        
        invalid_data = {
            "email": "invalid-email",
            "password": "123"
        }
        
        response = self.client.post(
            self.register_url,
            invalid_data,
            format='json'
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('firebase_admin.auth.get_user_by_email')
    @patch('posts.models.user.User.get_by_uid')
    @patch('requests.post')
    def test_login_success(self, mock_requests_post, mock_get_user, mock_get_firebase_user):
        print("\nTesting user login...")
        
        mock_firebase_user = MagicMock()
        mock_firebase_user.uid = "test123"
        mock_get_firebase_user.return_value = mock_firebase_user
        
        mock_user = MagicMock()
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_get_user.return_value = mock_user
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"idToken": "mock-firebase-token"}
        mock_requests_post.return_value = mock_response
        
        response = self.client.post(
            self.login_url,
            self.login_data,
            format='json'
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.login_data["email"])
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        print("\nTesting login with invalid credentials...")
        
        invalid_credentials = {
            "email": "wrong@email.com",
            "password": "wrongpass"
        }
        
        response = self.client.post(
            self.login_url,
            invalid_credentials,
            format='json'
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_login_missing_fields(self):
        print("\nTesting login with missing fields...")
        
        response = self.client.post(
            self.login_url,
            {},
            format='json'
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)