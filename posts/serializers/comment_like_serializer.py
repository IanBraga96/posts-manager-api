from rest_framework import serializers


class CommentLikeSerializer(serializers.Serializer):
    comment_id = serializers.CharField()
    user_id = serializers.CharField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {
            "comment_id": instance.comment_id,
            "user_id": instance.user_id,
            "created_at": instance.created_at,
        }
