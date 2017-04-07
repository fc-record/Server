from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from config import settings
from diary.models import Diary, Post, PostPhoto
from diary.serializers import DiarySerializer, PostSerializer, \
    PostPhotoSerializer

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PostPhotoViewSet(viewsets.ModelViewSet):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        photos = request.FILES.getlist('photo')
        photo_list = []
        for photo in photos:
            gps = self.get_gps_location(photo)
            serializer = self.get_serializer(data={'post': request.data['post'],
                                                   'photo': photo})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            photo_list.append(serializer.data['photo'])
        headers = self.get_success_headers(serializer.data)
        return Response(data={'post': serializer.data['post'],
                              'photo': str(photo_list),
                              'gpsLatitude': serializer.data['gpsLatitude'],
                              'gpsLongitude': serializer.data['gpsLongitude']},
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_gps_location(self, photo):
        img_path = settings.MEDIA_URL+'post/{}'.format(photo)
        print(img_path)
