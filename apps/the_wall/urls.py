from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^processPost/$', views.processPost),
    url(r'^processComment/(?P<post_id>[0-9]\d*)/$', views.processComment),
    url(r'^getComments/(?P<post_id>[0-9]\d*)/$', views.getComments),
]