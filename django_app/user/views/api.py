import json

from django.core import validators
from django.core.exceptions import ValidationError
from rest_auth.utils import default_create_token
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..serializers import UserSerializer
from ..models import Member

__all__ = (
    'UserViewSet',
)


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_create_token(Token, user, serializer)
        return token

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['user_type'] == 'NORMAL' or 'GOOGLE':
            email_valid = validators.validate_email
            try:
                email_valid(serializer.validated_data['username'])
            except ValidationError as e:
                return Response(data={'email': e.message}, status=status.HTTP_400_BAD_REQUEST)
        token = self.perform_create(serializer)
        # serialized_data = serializer.data
        # serialized_data['key'] = str(user.auth_token)
        # print(serialized_data)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'user': serializer.data,
                              'token': str(token)
                              }, status=status.HTTP_201_CREATED, headers=headers)
