from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import pockets


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', pockets.index, name='index'),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^content/', include('content.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static', (
            r'^media/(?P<path>.*)', 'serve', {
                'document_root': settings.MEDIA_ROOT
            }
        ),
        )