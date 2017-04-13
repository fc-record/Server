from django.contrib.auth import authenticate, logout, login
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import exceptions, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_temporary_tokens.models import TemporaryToken

from ..serializers import UserSerializer, TokenSerializer
from ..models import Member

__all__ = (
    'UserViewSet',
    'TokenViewSet',
    'LoginAPIView',
    'LogoutAPIView',
)


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        user = serializer.save()
        token = TemporaryToken.objects.create(user=user)
        login(self.request, user)
        return token.key

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

    def update(self, request, *args, **kwargs):
        user = request.user
        change_password1 = request.POST['change_password1']
        change_password2 = request.POST['change_password2']
        if change_password1 == change_password2:
            user.set_password(change_password1)
            user.save()
            return Response(status=status.HTTP_200_OK, data={'detail': 'Password change succeeded.'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'The password is different.'})


class TokenViewSet(GenericViewSet,
                   CreateModelMixin):
    queryset = TemporaryToken.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'

    def create(self, request, *args, **kwargs):
        key = request.POST['key']
        try:
            token = TemporaryToken.objects.get(key=key)
        except TemporaryToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        if token.expired:
            raise exceptions.AuthenticationFailed('Token has expired')
        else:
            return Response(status=status.HTTP_200_OK, data={'detail': 'valid token'})


class LoginAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        token, _ = TemporaryToken.objects.get_or_create(user=user)
        return Response(status=status.HTTP_200_OK, data={'key': token.key})


class LogoutAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        token = TemporaryToken.objects.get(user=user)
        logout(request)
        token.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Logout Succeeded and Token Delete'})
