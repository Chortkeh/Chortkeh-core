from rest_framework import serializers


class CreateAccountSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150, blank=True, null=True)


class UpdateAccountSerializer(serializers.Serializer):

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150, blank=True, null=True)
