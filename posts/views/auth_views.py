from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from ..models.user import User
from ..serializers.user_serializer import UserSerializer, UserResponseSerializer
from ..utils.firebase_utils import get_firebase_credentials
import requests


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.create(
                    name=serializer.validated_data["name"],
                    email=serializer.validated_data["email"],
                    password=serializer.validated_data["password"],
                )

                token = auth.create_custom_token(user.uid)

                response_data = {
                    "uid": user.uid,
                    "name": user.name,
                    "email": user.email,
                    "token": token.decode(),
                }

                return Response(
                    UserResponseSerializer(response_data).data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = auth.get_user_by_email(email)

            firebase_api_key = get_firebase_credentials()

            auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"

            auth_data = {
                "email": email,
                "password": password,
                "returnSecureToken": True,
            }

            auth_response = requests.post(auth_url, json=auth_data)

            if auth_response.status_code != 200:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            auth_result = auth_response.json()
            user_data = User.get_by_uid(user.uid)

            response_data = {
                "uid": user.uid,
                "name": user_data.name,
                "email": user_data.email,
                "token": auth_result["idToken"],
            }

            return Response(UserResponseSerializer(response_data).data)
        except Exception as e:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
