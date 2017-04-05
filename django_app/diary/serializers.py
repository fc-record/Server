from rest_framework import serializers

from diary.models import Diary, Post, PostPhoto
from user.serializers import UserSerializer


class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = (
            'post',
            'photo',
        )


class PostSerializer(serializers.ModelSerializer):
    photo_list = PostPhotoSerializer(many=True, read_only=True,
                                     source='postphoto_set')

    class Meta:
        model = Post
        fields = (
            'diary',
            'photo_list',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )


class DiarySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    diary = PostSerializer(many=True, read_only=True, source='post_set')

    class Meta:
        model = Diary
        fields = (
            'pk',
            'author',
            'diary',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )


"""
메타 클래스에 fields값을 pk로 줄지 diary로 줄지 고민됩니다.
"""
