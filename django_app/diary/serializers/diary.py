from rest_framework import serializers

from diary.models import Diary
from diary.serializers.post import PostSerializer
from user.serializers import UserSerializer

__all__ = (
    'DiarySerializer',
)


class DiarySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    # post = PostSerializer(many=True, read_only=True, source='post_set')
    post_count = serializers.ReadOnlyField(source='post_set.count', read_only=True)

    class Meta:
        model = Diary
        fields = (
            'pk',
            'title',
            'author',
            'post_count',
            'start_date',
            'end_date',
            'cover_image'
        )
        read_only_fields = (
            'post_count',
        )
