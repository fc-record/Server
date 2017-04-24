import requests
from django.contrib.auth import authenticate
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework_temporary_tokens.models import TemporaryToken

from config import settings
from utils import customexception, CheckSocialAccessToken, ImageValidate
from .models import Member


class NormalUserCreateSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='NORMAL', max_length=10)
    username = serializers.CharField(max_length=100, required=True,
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
        email_valid = validators.validate_email
        try:
            email_valid(validated_data['username'])
        except ValidationError as e:
            raise customexception.ValidationException(e.message)
        if 'password' in validated_data.keys():
            password = validated_data.pop('password')
            user = Member(**validated_data)
            user.set_password(password)
            user.save()
        elif 'password' not in validated_data.keys():
            raise customexception.ValidationException('Normal user required Password')
        return user


class FacebookUserCreateSerializer(NormalUserCreateSerializer):
    access_token = serializers.CharField(max_length=200, required=True,
                                         validators=[UniqueValidator(queryset=Member.objects.all())])

    def create(self, validated_data):
        access_token_validation = CheckSocialAccessToken.check_facebook(access_token=validated_data['access_token'])
        if access_token_validation:
            user = Member(**validated_data)
            user.save()
        else:
            raise customexception.AuthenticateException('Invalid Access Token')
        return user

class GoogleUserCreateSerializer(NormalUserCreateSerializer):
    access_token = serializers.CharField(max_length=200, required=True,
                                         validators=[UniqueValidator(queryset=Member.objects.all())])

    def create(self, validated_data):
        access_token_validation = CheckSocialAccessToken.check_google(access_token=validated_data['access_token'])
        if access_token_validation:
            user = Member(**validated_data)
            user.save()
        else:
            raise customexception.AuthenticateException('Invalid Access Token')
        return user


class ChangePasswordSerializer(serializers.Serializer):
    change_password1 = serializers.CharField(min_length=8, required=True)
    change_password2 = serializers.CharField(min_length=8, required=True)

    def create(self, validated_data):
        user_object = self.context['request'].user
        change_password1 = validated_data['change_password1']
        change_password2 = validated_data['change_password2']
        if change_password1 == change_password2 and len(change_password1) > 7:
            user_object.set_password(change_password1)
            user_object.save()
            return True
        else:
            raise customexception.AuthenticateException('Password does not match or too short password')


class TokenSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = Token
        fields = (
            'key',
        )

    def create(self, validated_data):
        key = validated_data['key']
        try:
            token = TemporaryToken.objects.get(key=key)
            user_object = token.user
            user = NormalUserCreateSerializer(user_object)
        except TemporaryToken.DoesNotExist:
            raise customexception.AuthenticateException('Invalid token')
        if token.expired:
            token.delete()
            raise customexception.AuthenticateException('Token has expired')
        else:
            token.expires = timezone.now() + timezone.timedelta(
                    minutes=settings.REST_FRAMEWORK_TEMPORARY_TOKENS['MINUTES'])
            return user


class ChangeProfileImageSerializer(serializers.Serializer):
    photo = serializers.ImageField()

    def create(self, validated_data):
        user_object = self.context['request'].user
        profile_img = validated_data['photo']
        if ImageValidate.imagevalidate(profile_img):
            user_object.profile_img = profile_img
            user_object.save()
            user = NormalUserCreateSerializer(user_object)
            return user
        else:
            raise customexception.ValidationException("It's not valid Extension")


class ChangePersonalSerializer(serializers.Serializer):
    hometown = serializers.CharField(max_length=50, required=False)
    nickname = serializers.CharField(max_length=20, required=False, validators=[UniqueValidator(queryset=Member.objects.all())])
    introduction = serializers.CharField(max_length=140, required=False)

    def create(self, validated_data):
        user_object = self.context['request'].user
        for keys in validated_data.keys():
            if keys == 'hometown':
                user_object.hometown = validated_data['hometown']
            elif keys == 'introduction':
                user_object.introduction = validated_data['introduction']
            elif keys == 'nickname':
                user_object.nickname = validated_data['nickname']
        user_object.save()
        user = NormalUserCreateSerializer(user_object)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    user_type = serializers.CharField(max_length=10, required=True)

    class Meta:
        fields = (
            'username',
            'password'
        )

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_object = authenticate(username=username, password=password)
        if user_object is None:
            raise customexception.AuthenticateException('Username or Password is wrong')
        return user_object


class FacebookLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    access_token = serializers.CharField(max_length=200, required=True, write_only=True)
    user_type = serializers.CharField(max_length=10, required=True)

    class Meta:
        fields = (
            'username',
            'access_token'
        )

    def create(self, validated_data):
        username = validated_data['username']
        access_token = validated_data['access_token']
        access_token_is_valid = CheckSocialAccessToken.check_facebook(access_token)
        if access_token_is_valid:
            user_object = Member.objects.get(username=username)
            user_object.access_token = access_token
            user_object.save()
            return user_object
        else:
            raise customexception.AuthenticateException('Invalid Access Token')


class GoogleLoginSerializer(FacebookLoginSerializer):
    def create(self, validated_data):
        username = validated_data['username']
        access_token = validated_data['access_token']
        access_token_is_valid = CheckSocialAccessToken.check_google(access_token)
        if access_token_is_valid:
            user_object = Member.objects.get(username=username)
            user_object.access_token = access_token
            user_object.save()
            return user_object
        else:
            raise customexception.AuthenticateException('Invalid Access Token')
