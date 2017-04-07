import piexif
from rest_framework import serializers

from config import settings
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
            'pk'
        )

    def create(self, validated_data):
        photo = validated_data['photo']
        postphoto = PostPhoto.objects.create(**validated_data)
        gps = self.get_gps_location(photo)
        postphoto.gpsLatitude = gps[0]
        postphoto.gpsLongitude = gps[1]
        postphoto.save()
        return postphoto

    @staticmethod
    def get_gps_location(photo):
        img_path = settings.MEDIA_ROOT + '/post/{}'.format(photo)
        try:
            exif_dict = piexif.load(img_path)
            gps_data = exif_dict['GPS']
            latetude = (gps_data[2][0][0]) + (gps_data[2][1][0] / 60 + (gps_data[2][2][0]) / 360000)
            longitude = (gps_data[4][0][0]) + (gps_data[4][1][0] / 60 + (gps_data[4][2][0]) / 360000)
            result = (round(latetude, 4), round(longitude, 4))
        except:
            latetude = None
            longitude = None
            result = (latetude, longitude)

        return result
