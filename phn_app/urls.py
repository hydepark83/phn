from django.conf.urls.defaults import *
from phn.views import *
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', index),
	url(r'^index/$', index),
	url(r'^update_user_disease_list/$', update_user_disease_list),
	url(r'^phn/$', phn_news),
)
