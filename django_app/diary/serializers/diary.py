from rest_framework import serializers

from diary.models import Diary
from diary.serializers import PostSerializer
from user.serializers import UserSerializer

__all__ = (
    "DiarySerializer",
)


class DiarySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    post = PostSerializer(many=True, read_only=True, source='post_set')

    class Meta:
        model = Diary
        fields = (
            'pk',
            'title',
            'author',
            'post',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )

