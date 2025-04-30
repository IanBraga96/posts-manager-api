from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import PostLike
from ..serializers.post_like_serializer import PostLikeSerializer
from ..middleware.auth_middleware import firebase_auth_middleware
from ..utils.api_utils import verify_post_exists


class PostLikeAPIView(APIView):
    @firebase_auth_middleware
    def post(self, request, pk):
        if not verify_post_exists(pk):
            return Response({"detail": "Post not found"}, status=404)

        user_id = request.user_id
        existing_like = PostLike.get(pk, user_id)

        if existing_like:
            PostLike.delete(pk, user_id)
            return Response({"detail": "Like removed"}, status=200)
        else:
            like = PostLike.create(pk, user_id)
            serializer = PostLikeSerializer(like)
            return Response(serializer.data, status=201)
