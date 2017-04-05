from django.conf import settings
from django.db import models


class Diary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                               default=None)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pk',)


class Post(models.Model):
    diary = models.ForeignKey(Diary)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'diary'


class PostPhoto(models.Model):
    post = models.ForeignKey(Post)
    photo = models.ImageField(upload_to='post')

    class Meta:
        order_with_respect_to = 'post'
