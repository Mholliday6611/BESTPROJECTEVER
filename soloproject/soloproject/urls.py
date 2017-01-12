from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('appone.urls')),
)