from rest_framework import serializers

from diary.models import Post
from diary.serializers.post_photo import PostPhotoSerializer

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    photo_list = PostPhotoSerializer(many=True, read_only=True,
                                     source='postphoto_set')

    class Meta:
        model = Post
        fields = (
            'pk',
            'diary',
            'content',
            'created_date',
            'cover_image',
            'photo_list',
        )
        read_only_fields = (
            'created_date',
        )
