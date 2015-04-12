from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'meliscore.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'front.views.home', name='home'),
    url(r'^score/(?P<itemid>[\S]+)$', 'front.views.score', name='score'),
    url(r'^score/$', 'front.views.score', name='score'),
    url(r'^sweetspot/(?P<itemid>[\S]+)$', 'front.views.sweetspot', name='sweetspot'),
    url(r'^salespeed/(?P<itemid>[\S]+)$', 'front.views.salespeed', name='salespeed'),

    url(r'^admin/', include(admin.site.urls)),
]
