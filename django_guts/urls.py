from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^(?P<app>[^/]+)(?P<cwd>.*/)(?P<leaf>[^/]*)$', 'django_guts.views.app_guts', name='app-guts'),
     url(r'^(?P<app>[^/]+)$', 'django_guts.views.app_guts', name='app-guts'),
     url(r'^$', 'django_guts.views.apps', name='index'),
)
