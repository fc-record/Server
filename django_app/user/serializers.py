import requests
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from config import settings
from utils import customexception, CheckSocialAccessToken
from .models import Member


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='NORMAL')
    username = serializers.CharField(max_length=20, required=True,
                                     validators=[UniqueValidator(queryset=Member.objects.all())])
    nickname = serializers.CharField(max_length=50, allow_null=True, required=False)
    password = serializers.CharField(min_length=8, max_length=20, write_only=True, required=False)

    class Meta:
        model = Member

        fields = (
            'username',
            'nickname',
            'password',
            'user_type',
            'access_token',
            'profile_img',
            'hometown',
            'introduction',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'access_token': {'write_only': True},
            'introduction': {'max_length': 140}
        }

    # api.py create메소드의 perform_create의 serializer.save()호출 시 실행
    def create(self, validated_data):
        user_type = validated_data['user_type']
        if user_type == 'FACEBOOK' or user_type == 'GOOGLE':
            access_token_validation = CheckSocialAccessToken.check_facebook(access_token=validated_data['access_token'])
            if access_token_validation:
                pass
            else:
                raise customexception.ValidationException('Invalid Access Token')
        if user_type == 'NORMAL' or user_type == 'GOOGLE':
            email_valid = validators.validate_email
            try:
                email_valid(validated_data['username'])
            except ValidationError as e:
                raise customexception.ValidationException(e.message)
            if user_type == 'NORMAL' and 'password' in validated_data.keys():
                password = validated_data.pop('password')
                user = Member(**validated_data)
                user.save()
                user.set_password(password)
            elif user_type == 'NORMAL' and 'password' not in validated_data.keys():
                raise customexception.ValidationException('Normal user required Password')
            else:
                user = Member(**validated_data)
                user.save()
        else:
            user = Member(**validated_data)
            user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'key',
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        fields = (
            'username',
            'password'
        )


class SocialLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    access_token = serializers.CharField(max_length=200, required=True, write_only=True)

    class Meta:
        fields = (
            'username',
            'access_token'
        )