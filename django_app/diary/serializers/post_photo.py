from rest_framework import serializers

from diary.models import PostPhoto


class PostPhotoSerializer(serializers.ModelSerializer):
    gpsLatitude = serializers.FloatField()
    gpsLongitude = serializers.FloatField()

    class Meta:
        model = PostPhoto
        fields = (
            'post',
            'photo',
            'gpsLatitude',
            'gpsLongitude',
        )

