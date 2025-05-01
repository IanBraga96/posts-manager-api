import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.post_serializer import (
    PostSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
)
from ..middleware.auth_middleware import firebase_auth_middleware
from ..models.user import User


BASE_URL = "https://dev.codeleap.co.uk/careers/"


class PostListCreateAPIView(APIView):
    @firebase_auth_middleware
    def get(self, request):
        search_term = request.query_params.get("search", "").lower()
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                results = response.json()["results"]
                if search_term:
                    results = [
                        post
                        for post in results
                        if search_term in post.get("username", "").lower()
                        or search_term in post.get("title", "").lower()
                        or search_term in post.get("content", "").lower()
                    ]

                # results = sorted(results, key=lambda x: x['created_datetime'], reverse=True)

                serializer = PostSerializer(
                    results,
                    many=True,
                    context={"request": request, "user_id": request.user_id},
                )
                return Response({"count": len(results), "results": serializer.data})
            return Response(
                {"detail": "Failed to fetch posts"}, status=response.status_code
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    @firebase_auth_middleware
    def post(self, request):
        user = User.get_by_uid(request.user_id)
        if not user:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        data["username"] = user.name

        serializer = PostCreateSerializer(data=data)
        if serializer.is_valid():
            try:
                response = requests.post(BASE_URL, json=serializer.validated_data)
                return Response(response.json(), status=response.status_code)
            except Exception as e:
                return Response({"detail": str(e)}, status=500)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    def get_url(self, pk):
        return f"{BASE_URL}{pk}/"

    @firebase_auth_middleware
    def get(self, request, pk):
        try:
            response = requests.get(self.get_url(pk))
            if response.status_code == 200:
                serializer = PostSerializer(
                    response.json(),
                    context={"request": request, "user_id": request.user_id},
                )
                return Response(serializer.data)
            return Response({"detail": "Post not found"}, status=response.status_code)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    @firebase_auth_middleware
    def patch(self, request, pk):
        serializer = PostUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = requests.patch(
                    self.get_url(pk), json=serializer.validated_data
                )
                return Response(response.json(), status=response.status_code)
            except Exception as e:
                return Response({"detail": str(e)}, status=500)
        return Response(serializer.errors, status=400)

    @firebase_auth_middleware
    def delete(self, request, pk):
        try:
            response = requests.delete(self.get_url(pk))
            return Response(status=response.status_code)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
