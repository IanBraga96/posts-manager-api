from rest_framework import serializers
from posts.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["post_id", "username", "created_at"]
