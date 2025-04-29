from rest_framework import serializers


class PostLikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    username = serializers.CharField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {
            "post_id": instance.post_id,
            "username": instance.username,
            "created_at": instance.created_at,
        }
