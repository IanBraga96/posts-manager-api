from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)


class UserResponseSerializer(serializers.Serializer):
    uid = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    token = serializers.CharField()
