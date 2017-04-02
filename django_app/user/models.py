from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    USER_TYPE_CHOICES = (
        ('GOOGLE', 'google'),
        ('FACEBOOK', 'facebook'),
        ('NORMAL', 'normal')
    )
    nickname = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='normal')
    access_token = models.CharField(max_length=100)

    REQUIRED_FIELDS = []
