from django.shortcuts import render

# Create your views here.
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

BASE_URL = "https://dev.codeleap.co.uk/careers/"

class PostListCreateAPIView(APIView):
    """
    API view to list all posts
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