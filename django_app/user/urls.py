from django.conf.urls import url
from .views import api

urlpatterns = [
    url(r'^login/$', api.LoginAPIView.as_view()),
    url(r'^logout/$', api.LogoutAPIView.as_view()),
    url(r'^token/$', api.CheckToken.as_view()),
    url(r'^changeprofile/$', api.ChangeProfileImage.as_view()),
    url(r'^changepassword/$', api.ChangePassword.as_view()),
]