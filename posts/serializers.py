from rest_framework import serializers
from .models import PostLike, PostComment


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["post_id", "username", "created_at"]


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


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    created_datetime = serializers.DateTimeField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def to_representation(self, instance):
        if not isinstance(instance, dict):
            instance = {
                "id": instance.id,
                "username": instance.username,
                "title": instance.title,
                "content": instance.content,
                "created_datetime": instance.created_datetime,
            }

        data = {
            "id": instance.get("id"),
            "username": instance.get("username"),
            "title": instance.get("title"),
            "content": instance.get("content"),
            "created_datetime": instance.get("created_datetime"),
        }

        data["likes_count"] = self.get_likes_count(instance)
        data["is_liked"] = self.get_is_liked(instance)

        return data

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post_id=obj.get("id")).count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.data.get("username"):
            return PostLike.objects.filter(
                post_id=obj.get("id"), username=request.data.get("username")
            ).exists()
        return False


class PostCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
