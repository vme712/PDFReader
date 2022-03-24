from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'token', 'username', 'is_active', 'password', ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        update_last_login(None, user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'Не заполенно поле username'
            )
        if password is None:
            raise serializers.ValidationError(
                'Не заполенно поле Password'
            )
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с этим username и паролем не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Этот пользователь был деактивирован.'
            )
        update_last_login(None, user)
        return {'token': user.token, 'id': user.id}

    class Meta:
        model = User


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', )
