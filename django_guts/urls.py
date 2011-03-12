from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^/$', 'django_guts.views.empty_view'),
)
