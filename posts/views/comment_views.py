from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import PostComment
from ..serializers.post_comment_serializer import PostCommentSerializer
from ..utils.utils import extract_mentions


class PostCommentAPIView(APIView):
    def get(self, request, pk):
        comments = PostComment.objects.filter(post_id=pk)
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        username = request.data.get("username")
        content = request.data.get("content")
        if not username or not content:
            return Response({"detail": "Username and content are required"}, status=400)

        mentioned_users = extract_mentions(content)
        comment = PostComment.objects.create(
            post_id=pk,
            username=username,
            content=content,
            mentioned_users=mentioned_users,
        )
        serializer = PostCommentSerializer(comment)
        return Response(serializer.data, status=201)

    def patch(self, request, pk):
        comment_id = request.data.get("comment_id")
        username = request.data.get("username")
        content = request.data.get("content")

        if not all([comment_id, username, content]):
            return Response({"detail": "Missing fields"}, status=400)

        try:
            comment = PostComment.objects.get(id=comment_id, post_id=pk)
        except PostComment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=404)

        if comment.username != username:
            return Response({"detail": "Not your comment"}, status=403)

        comment.content = content
        comment.mentioned_users = extract_mentions(content)
        comment.save()
        return Response(PostCommentSerializer(comment).data)

    def delete(self, request, pk):
        comment_id = request.data.get("comment_id")
        username = request.data.get("username")
        if not all([comment_id, username]):
            return Response({"detail": "Missing fields"}, status=400)

        try:
            comment = PostComment.objects.get(id=comment_id, post_id=pk)
        except PostComment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=404)

        if comment.username != username:
            return Response({"detail": "Not your comment"}, status=403)

        comment.delete()
        return Response(status=204)
