from rest_framework import serializers
from posts.models import PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = [
            "id",
            "post_id",
            "username",
            "content",
            "created_at",
            "mentioned_users",
        ]
