from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^visual/', include('visual.urls')),
    url(r'^alg/', include('alg.urls')),
]

