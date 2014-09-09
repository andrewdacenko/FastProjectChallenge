from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.main.views.index', name='index'),
    url(r'^topic/(?P<topic_id>\d+)$', 'apps.main.views.topic'),
    url(r'^active/$', 'apps.main.views.state'),
    url(r'^voting/$', 'apps.main.views.state'),
    url(r'^archive/$', 'apps.main.views.state'),

    url(r'^login/$', 'apps.guest.views.login', name='login'),
    url(r'^auth/$', 'apps.guest.views.auth', name='auth'),
    url(r'^logout/$', 'apps.guest.views.logout', name='logout'),
    url(r'^register/$', 'apps.guest.views.register_user', name='register_user'),

    url(r'^api/', include('apps.api.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
