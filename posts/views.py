from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostCreateSerializer

BASE_URL = "https://dev.codeleap.co.uk/careers/"

class PostListCreateAPIView(APIView):
    """
    API view to list all posts and create a new post
    """

    def get(self, request):
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(
                {"detail": "Failed to fetch posts from external API"},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = requests.post(BASE_URL, json=serializer.validated_data)
                if response.status_code in [201, 200]:
                    return Response(response.json(), status=response.status_code)
                return Response(
                    {"detail": "Failed to create post on external API"},
                    status=response.status_code,
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    """
    API view to retrieve a single post by ID
    """

    def get_url(self, pk):
        return f"{BASE_URL}{pk}/"

    def get(self, request, pk):
        try:
            response = requests.get(self.get_url(pk))
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            return Response(
                {"detail": "Post not found or error fetching from external API"},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )