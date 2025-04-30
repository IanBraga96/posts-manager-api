from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import PostComment
from ..serializers.post_comment_serializer import PostCommentSerializer
from ..utils.utils import extract_mentions
from ..middleware.auth_middleware import firebase_auth_middleware


class PostCommentAPIView(APIView):
    @firebase_auth_middleware
    def get(self, request, pk):
        comments = PostComment.list_by_post(pk)
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @firebase_auth_middleware
    def post(self, request, pk):
        user_id = request.user_id
        content = request.data.get("content")
        
        if not content:
            return Response({"detail": "Content is required"}, status=400)

        mentioned_users = extract_mentions(content)
        comment = PostComment.create(
            post_id=pk,
            user_id=user_id,
            content=content,
            mentioned_users=mentioned_users,
        )
        serializer = PostCommentSerializer(comment)
        return Response(serializer.data, status=201)

    @firebase_auth_middleware
    def patch(self, request, pk):
        comment_id = request.data.get("comment_id")
        content = request.data.get("content")

        if not all([comment_id, content]):
            return Response({"detail": "Missing fields"}, status=400)

        comment = PostComment.get(comment_id)
        if not comment:
            return Response({"detail": "Comment not found"}, status=404)

        if comment.user_id != request.user_id:
            return Response({"detail": "Not your comment"}, status=403)

        mentioned_users = extract_mentions(content)
        updated_comment = comment.update(content, mentioned_users)
        return Response(PostCommentSerializer(updated_comment).data)

    @firebase_auth_middleware
    def delete(self, request, pk):
        comment_id = request.data.get("comment_id")

        if not comment_id:
            return Response({"detail": "Comment ID is required"}, status=400)

        comment = PostComment.get(comment_id)
        if not comment:
            return Response({"detail": "Comment not found"}, status=404)

        if comment.user_id != request.user_id:
            return Response({"detail": "Not your comment"}, status=403)

        PostComment.delete(comment_id)
        return Response(status=204)
