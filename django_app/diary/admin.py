from django.contrib import admin

from diary.models import Diary, Post, PostPhoto

admin.site.register(Diary)
admin.site.register(Post)
admin.site.register(PostPhoto)