from django.conf import settings
from django.db import models


class Diary(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pk',)


class Post(models.Model):
    diary = models.ForeignKey(Diary)
    content = models.TextField()
    photo = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'diary'
