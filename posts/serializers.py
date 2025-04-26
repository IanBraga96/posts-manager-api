from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    created_datetime = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance
        return {
            "id": instance.id,
            "username": instance.username,
            "title": instance.title,
            "content": instance.content,
            "created_datetime": instance.created_datetime,
        }
    
class PostCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()