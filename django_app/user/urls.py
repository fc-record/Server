from django.conf.urls import url
from .views import api

urlpatterns = [
    url(r'^login/$', api.LoginAPIView.as_view()),
    url(r'^logout/$', api.LogoutAPIView.as_view())
]