
from django.http import HttpResponse
from django.conf.urls.defaults import patterns, include, url
from mockapi.api import v0_api

def render_null(request):
    return HttpResponse('')
    
urlpatterns = patterns('',
    url(r'^api/', include(v0_api.urls)),
    url(r'^favicon.ico/$', render_null),
)
