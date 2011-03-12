from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^django_guts/', include('django_guts.urls')),
)

