from rest_framework import generics
from rest_framework import permissions

from diary.models import Diary, Post, PostPhoto
from diary.serializers import DiarySerializer, PostSerializer, \
    PostPhotoSerializer

__all__ = (
    'DiaryCreate',
    'DiaryDestroy',
    'DiaryList',
    'DiaryDetail',

    'PostCreate',
    'PostDestroy',
    'PostList',
    'PostDetail',

    'PostPhotoCreate',
    'PostPhotoDestroy',
)


class DiaryCreate(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer


class DiaryDestroy(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer


"""
pagination 추가할지 고민중
"""


class DiaryList(generics.ListCreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DiaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostPhotoCreate(generics.CreateAPIView):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer


class PostPhotoDestroy(generics.DestroyAPIView):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
