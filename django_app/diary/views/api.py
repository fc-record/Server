from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view

from diary.models import Diary, Post, PostPhoto
from diary.serializers import DiarySerializer, PostSerializer, \
    PostPhotoSerializer
from user.serializers import UserSerializer

__all__ = (
    'DiaryViewSet',
    'PostViewSet',
    'PostPhotoViewSet',
)


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        # def create(self, request, *args, **kwargs):
        #     serializer = self.get_serializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)

    # @api_view(['POST'])
    # def current_user(request):
    #     serializer = UserSerializer(request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostPhotoViewSet(viewsets.ModelViewSet):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# class DiaryCreate(generics.CreateAPIView):
#     queryset = Diary.objects.all()
#     serializer_class = DiarySerializer
#
#
# class DiaryDestroy(generics.DestroyAPIView):
#     queryset = Diary.objects.all()
#     serializer_class = DiarySerializer
#
#
# """
# pagination 추가할지 고민중
# """
#
#
# class DiaryList(generics.ListCreateAPIView):
#     queryset = Diary.objects.all()
#     serializer_class = DiarySerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class DiaryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Diary.objects.all()
#     serializer_class = DiarySerializer

#
# class PostCreate(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostDestroy(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostPhotoCreate(generics.CreateAPIView):
#     queryset = PostPhoto.objects.all()
#     serializer_class = PostPhotoSerializer
#
#
# class PostPhotoDestroy(generics.DestroyAPIView):
#     queryset = PostPhoto.objects.all()
#     serializer_class = PostPhotoSerializer
