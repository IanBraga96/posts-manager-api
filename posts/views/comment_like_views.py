from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CommentLike, PostComment
from ..serializers.comment_like_serializer import CommentLikeSerializer
from ..middleware.auth_middleware import firebase_auth_middleware


class CommentLikeAPIView(APIView):
    @firebase_auth_middleware
    def post(self, request, comment_id):
        comment = PostComment.get(comment_id)
        if not comment:
            return Response({"detail": "Comment not found"}, status=404)

        user_id = request.user_id
        existing_like = CommentLike.get(comment_id, user_id)

        if existing_like:
            CommentLike.delete(comment_id, user_id)
            return Response({"detail": "Like removed"}, status=200)
        else:
            like = CommentLike.create(comment_id, user_id)
            serializer = CommentLikeSerializer(like)
            return Response(serializer.data, status=201)
