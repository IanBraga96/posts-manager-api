from rest_framework import serializers
from posts.models import PostComment


class PostCommentSerializer(serializers.Serializer):
    id = serializers.CharField()
    post_id = serializers.IntegerField()
    username = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    mentioned_users = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "post_id": instance.post_id,
            "username": instance.username,
            "content": instance.content,
            "created_at": instance.created_at,
            "mentioned_users": instance.mentioned_users,
        }
