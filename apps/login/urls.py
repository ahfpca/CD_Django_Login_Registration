from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'check$', views.check),
    url(r'logout$', views.logout),
    url(r'success$', views.success),
    url(r'register$', views.register),
    url(r'$', views.index),
]
