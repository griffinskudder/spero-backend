from authentication.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'account_set')
        read_only_fields = ('id', 'account_set')


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_staff')
        read_only_fields = ('id', 'username', 'is_staff')
