from rest_framework import serializers


class PostLikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    user_id = serializers.CharField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {
            "post_id": instance.post_id,
            "user_id": instance.user_id,
            "created_at": instance.created_at,
        }
