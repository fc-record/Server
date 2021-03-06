from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MemberManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
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
    nickname = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='NORMAL')
    access_token = models.CharField(max_length=200, blank=True, null=True)
    profile_img = models.ImageField(blank=True, null=True)
    hometown = models.CharField(max_length=50, blank=True, null=True)
    introduction = models.CharField(max_length=140, blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='follower_set',
        through='RelationShip',
    )

    objects = MemberManager()

    USERNAME_FIELD = 'username'

    def follow(self, user):
        self.following_relations.create(
            to_user=user
        )

    def unfollow(self, user):
        self.following_relations.filter(
            to_user=user
        ).delete()


class RelationShip(models.Model):
    from_user = models.ForeignKey(Member, related_name='following_relations')
    to_user = models.ForeignKey(Member, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )
