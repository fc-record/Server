from rest_framework import serializers

from diary.models import PostPhoto

__all__ = (
    'PostPhotoSerializer',
)


class PostPhotoSerializer(serializers.ModelSerializer):
    # gpsLatitude = serializers.FloatField(required=False)
    # gpsLongitude = serializers.FloatField(required=False)

    class Meta:
        model = PostPhoto
        fields = (
            'post',
            'photo',
            'gpsLatitude',
            'gpsLongitude',
        )
