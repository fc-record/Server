from rest_auth.utils import default_create_token
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Member


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='NORMAL')
    username = serializers.CharField(max_length=20, required=True,
                                     validators=[UniqueValidator(queryset=Member.objects.all())])
    nickname = serializers.CharField(max_length=50, allow_blank=True)
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
            'introduction',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'access_token': {'write_only': True}
        }

    # api.py create메소드의 perform_create의 serializer.save()호출 시 실행
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Member(**validated_data)
        try:
            user.set_password(password)
        except KeyError:
            pass
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'key',
        )
