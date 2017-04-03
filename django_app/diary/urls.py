from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DiaryList.as_view(), name='diary-list'),
    url(r'^create/$', views.DiaryCreate.as_view(), name='diary-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.DiaryDetail.as_view(),
        name='diary-detail'),
    url(r'^(?P<pk>[0-9]+)/destroy/$', views.DiaryDestroy.as_view(),
        name='diary-destroy'),
    url(r'^post/$', views.PostList.as_view(), name='post-list'),
    url(r'^post/create/$', views.PostCreate.as_view(), name='post-create'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(),
        name='post-detail'),
    url(r'^post/(?P<pk>[0-9]+)/destroy/$', views.PostDestroy.as_view(),
        name='post-destroy'),
    url(r'^photo/$', views.PostPhotoCreate.as_view(), name='photo-create'),
    url(r'^photo/(?P<pk>[0-9]+)/$', views.PostPhotoDestroy.as_view(),
        name='photo-destroy'),
]
