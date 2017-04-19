from django.contrib.auth import authenticate, login
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_temporary_tokens.models import TemporaryToken
from ..serializers import UserSerializer, LoginSerializer
from ..models import Member
from config import customexception

__all__ = (
    'UserViewSet',
    'CheckToken',
    'ChangePassword',
    'ChangeProfileImage',
    'LoginAPIView',
    'LogoutAPIView',
    'ChangePersonal',
)


class UserViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        token = TemporaryToken.objects.create(user=user)
        return token.key

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['user_type'] == 'NORMAL' or serializer.validated_data['user_type'] == 'GOOGLE':
            email_valid = validators.validate_email
            try:
                email_valid(serializer.validated_data['username'])
            except ValidationError as e:
                raise customexception.ValidationException(e.message)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'user': serializer.data,
                              'key': str(token)
                              }, status=status.HTTP_201_CREATED, headers=headers)


class ChangePassword(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        change_password1 = request.POST['change_password1']
        change_password2 = request.POST['change_password2']
        if change_password1 == change_password2 and len(change_password1) > 7:
            user.set_password(change_password1)
            user.save()
            return Response(status=status.HTTP_200_OK, data={'detail': 'Password change succeeded.'})
        else:
            raise customexception.AuthenticateException('Password does not match or too short password')


class ChangeProfileImage(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def imagevalidate(self, filename):
        VALID_EXTENSION = [
            'jpg',
            'png'
        ]
        try:
            name, extention = filename.split('.')
            if extention.lower() in VALID_EXTENSION:
                return True
            else:
                return False
        except:
            raise customexception.ValidationException("It's not valid Extension")

    def post(self, request):
        user_object = request.user
        profile_img = request.FILES.get('photo')
        valid = self.imagevalidate(profile_img.name)
        if valid:
            user_object.profile_img = profile_img
            user_object.save()
            user = UserSerializer(user_object)
            return Response(status=status.HTTP_201_CREATED, data={'user': user.data})
        else:
            raise customexception.ValidationException("It's not valid Extension")


class ChangePersonal(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_object = request.user
        for keys in request.data.keys():
            if keys == 'hometown':
                user_object.hometown = request.POST['hometown']
            elif keys == 'introduction':
                user_object.introduction = request.POST['introduction']
            elif keys == 'nickname':
                user_object.nickname = request.POST['nickname']
        user_object.save()
        user = UserSerializer(user_object)
        return Response(status=status.HTTP_201_CREATED, data={'user': user.data})



class CheckToken(GenericAPIView):
    def post(self, request):
        key = request.POST['key']
        try:
            token = TemporaryToken.objects.get(key=key)
        except TemporaryToken.DoesNotExist:
            raise customexception.AuthenticateException('Invalid token')
        if token.expired:
            raise customexception.AuthenticateException('Token has expired')
        else:
            return Response(status=status.HTTP_200_OK, data={'detail': 'valid token'})


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print(request.data)
        user_object = authenticate(username=username, password=password)
        if user_object is None:
            raise customexception.AuthenticateException('Username or Password is wrong')
        token, _ = TemporaryToken.objects.get_or_create(user=user_object)
        user = UserSerializer(user_object)
        return Response(status=status.HTTP_200_OK, data={'user': user.data,
                                                         'key': token.key})


class LogoutAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        token = TemporaryToken.objects.get(user=user)
        token.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Logout Succeeded and Token Delete'})
