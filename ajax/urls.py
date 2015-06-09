from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
	url(r'^account_change/$',account_change),
)
