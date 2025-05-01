from rest_framework import serializers
from posts.models import PostLike, PostComment


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    created_datetime = serializers.DateTimeField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
            "likes_count": self.get_likes_count(instance),
            "is_liked": self.get_is_liked(instance),
            "comments_count": self.get_comments_count(instance),
        }
        return data

    def get_likes_count(self, obj):
        post_id = obj.get("id")
        likes = PostLike.list_by_post(post_id)
        return len(likes) if likes else 0

    def get_is_liked(self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            post_id = obj.get("id")
            return PostLike.get(post_id, user_id) is not None
        return False

    def get_comments_count(self, obj):
        post_id = obj.get("id")
        comments = PostComment.list_by_post(post_id)
        return len(comments) if comments else 0


class PostCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=False)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
