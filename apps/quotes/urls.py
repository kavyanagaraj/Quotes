from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^postquote$', views.postquote),
    url(r'^favquote/(?P<id>\d+)$', views.favquote),
    url(r'^users/(?P<id>\d+)$', views.userwall, name = "userwall"),
    url(r'^removefavquote/(?P<id>\d+)$', views.removefavquote),
]
