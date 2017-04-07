from rest_framework import serializers

from diary.models import PostPhoto

__all__ = (
    'PostPhotoSerializer',
)


class PostPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostPhoto
        fields = (
            'post',
            'photo',
            'gpsLatitude',
            'gpsLongitude',
            '_order'
        )
