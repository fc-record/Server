from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MemberManager(UserManager):
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, None, password, **extra_fields)


class Member(AbstractUser):
    USER_TYPE_CHOICES = (
        ('GOOGLE', 'google'),
        ('FACEBOOK', 'facebook'),
        ('NORMAL', 'normal')
    )
    nickname = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='NORMAL')
    access_token = models.CharField(max_length=128, blank=True)
    profile_img = models.ImageField(blank=True)
    introduction = models.CharField(max_length=140, blank=True)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
