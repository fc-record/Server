import requests
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from config import customexception
from config import settings
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
            'hometown': {'max_length': 140}
        }

    # api.py create메소드의 perform_create의 serializer.save()호출 시 실행
    def create(self, validated_data):
        user_type = validated_data['user_type']
        if user_type == 'FACEBOOK' or user_type == 'GOOGLE':
            access_token_validation = self.check_social_accesstoken(validated_data['access_token'])
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

    def check_social_accesstoken(self, access_token):
        param = {
            'input_token': access_token,
            'access_token': settings.CONFIG_FILE['facebook']['app-access-token']
        }
        response = requests.get('https://graph.facebook.com/debug_token', params=param)
        response_dict = response.json()
        is_valid = response_dict['data']['is_valid']
        return is_valid


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