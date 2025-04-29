from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import PostLike
from ..serializers.post_like_serializer import PostLikeSerializer


class PostLikeAPIView(APIView):
    def post(self, request, pk):
        username = request.data.get("username")
        if not username:
            return Response({"detail": "Username is required"}, status=400)

        existing_like = PostLike.get(pk, username)
        
        if existing_like:
            PostLike.delete(pk, username)
            return Response({"detail": "Like removed"}, status=200)
        else:
            like = PostLike.create(pk, username)
            serializer = PostLikeSerializer(like)
            return Response(serializer.data, status=201)
