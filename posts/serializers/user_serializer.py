from rest_framework import serializers
from email_validator import validate_email, EmailNotValidError


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_name(self, value):
        if " " in value:
            raise serializers.ValidationError("The name cannot contain spaces")
        return value

    def validate_email(self, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            return email_info.normalized
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))


class UserResponseSerializer(serializers.Serializer):
    uid = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    token = serializers.CharField()
