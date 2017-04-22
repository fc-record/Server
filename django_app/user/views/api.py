from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_temporary_tokens.models import TemporaryToken
from ..models import Member
from ..serializers import NormalUserCreateSerializer, FacebookUserCreateSerializer, LoginSerializer, TokenSerializer, \
    ChangePasswordSerializer, ChangeProfileImageSerializer, ChangePersonalSerializer, \
    LogoutSerializer, FacebookLoginSerializer, GoogleLoginSerializer, GoogleUserCreateSerializer

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
    serializer_class = NormalUserCreateSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.POST['user_type'] == 'NORMAL':
            return self.serializer_class
        elif self.request.POST['user_type'] == 'FACEBOOK':
            return FacebookUserCreateSerializer
        elif self.request.POST['user_type'] == 'GOOGLE':
            return GoogleUserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = TemporaryToken.objects.create(user=user)
        return token.key

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'user': serializer.data,
                              'key': str(token)
                              }, status=status.HTTP_201_CREATED, headers=headers)


class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            return Response(status=status.HTTP_200_OK, data={'detail': 'Password change succeeded.'})


class ChangeProfileImage(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangeProfileImageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'user': user.data})


class ChangePersonal(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePersonalSerializer

    def post(self, request):
        serializer = self.serializer_class
        serializer.is_valid(data=request.data, context={'request': request})
        user = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={'user': user.data})


class CheckToken(GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Valid Token',
                                                         'user': user.data})


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.POST['user_type'] == 'NORMAL':
            return self.serializer_class
        elif self.request.POST['user_type'] == 'FACEBOOK':
            return FacebookLoginSerializer
        elif self.request.POST['user_type'] == 'GOOGLE':
            return GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.save()
        token, exists = TemporaryToken.objects.get_or_create(user=user_object)
        if exists:
            pass
        elif token.expired:
            token.delete()
            token = TemporaryToken.objects.create(user=user_object)
        user = NormalUserCreateSerializer(user_object)
        return Response(status=status.HTTP_200_OK, data={'user': user.data,
                                                         'key': token.key})


class LogoutAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class
        serializer.is_valid(data=request.data)
        user = request.user
        token = TemporaryToken.objects.get(user=user)
        token.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Logout Succeeded and Token Delete'})
