from rest_framework import serializers
from posts.models import PostComment, CommentLike


class PostCommentSerializer(serializers.Serializer):
    id = serializers.CharField()
    post_id = serializers.IntegerField()
    user_id = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    mentioned_users = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "post_id": instance.post_id,
            "user_id": instance.user_id,
            "content": instance.content,
            "created_at": instance.created_at,
            "mentioned_users": instance.mentioned_users,
            "likes_count": self.get_likes_count(instance),
            "is_liked": self.get_is_liked(instance),
        }

    def get_likes_count(self, obj):
        likes = CommentLike.list_by_comment(obj.id)
        return len(likes)

    def get_is_liked(self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            return CommentLike.get(obj.id, user_id) is not None
        return False
