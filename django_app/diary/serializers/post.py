from rest_framework import serializers

from diary.models import Post
from diary.serializers import DiarySerializer, PostPhotoSerializer

__all__ = (
    "PostSerializer",
)


class PostSerializer(serializers.ModelSerializer):
    diary = DiarySerializer()
    title = serializers.CharField(max_length=100)
    photo_list = PostPhotoSerializer(many=True, read_only=True,
                                     source='postphoto_set')

    class Meta:
        model = Post
        fields = (
            'title',
            'photo_list',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )
