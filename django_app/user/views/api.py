import json

from django.core import validators
from django.core.exceptions import ValidationError
from rest_auth.utils import default_create_token
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from ..serializers import UserSerializer, TokenSerializer
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
        if serializer.validated_data['user_type'] == 'NORMAL' or serializer.validated_data['user_type'] == 'GOOGLE':
            email_valid = validators.validate_email
            try:
                email_valid(serializer.validated_data['username'])
            except ValidationError as e:
                return Response(data={'email': e.message}, status=status.HTTP_400_BAD_REQUEST)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'user': serializer.data,
                              'key': str(token)
                              }, status=status.HTTP_201_CREATED, headers=headers)


class TokenViewSet(GenericViewSet,
                   CreateModelMixin):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'

    def create(self, request, *args, **kwargs):
        token = request.POST['key']
        if Token.objects.filter(key=token).exists():
            return Response(data={'key': 'valid token'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'key': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
