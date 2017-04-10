"""record URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views
from rest_framework import routers


from diary.views.api import DiaryViewSet as diary_api_DiaryViewSet
from diary.views.api import PostPhotoViewSet as diary_api_PostPhotoViewSet
from diary.views.api import PostViewSet as diary_api_PostViewSet
from user.views.api import UserViewSet as user_api_UserViewSet

router = routers.DefaultRouter()
router.register(r'users', user_api_UserViewSet)
router.register(r'diary/diary', diary_api_DiaryViewSet)
router.register(r'diary/post', diary_api_PostViewSet)
router.register(r'diary/postphoto', diary_api_PostPhotoViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^user/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += [url(
        r'static/(?P<path>.*)$', views.serve),
    ]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
