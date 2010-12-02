from django.conf.urls.defaults import *
from django.conf import settings
from django.template import add_to_builtins

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    (r'^users/', include('users.urls')),
    (r'^questions/', include('quest.urls')),
)

urlpatterns += patterns('users.views',
    (r'^$', 'view_homepage', {'homepage_template':'homepage.html'}, 'homepage'),
    (r'^notepad/$', 'view_notepad', {'notepad_template':'notepad.html'}, 'notepad'),
    (r'^notepad/preview/$', 'view_notepad_preview', {'notepad_preview_template':'notepad.html'}, 'notepad_preview'),
)

urlpatterns += patterns('users.views',
    (r'^accounts/register/$', 'view_register', {'registration_template': 'register.html'}, 'register'),
    (r'^accounts/login/$', 'view_login', {'login_template': 'login.html'}, 'login'),
    (r'^accounts/logout/$', 'view_logout', {'logout_template': 'logout.html'}, 'logout'),
    (r'^settings/$', 'view_account_settings', {'settings_template':''}, 'settings'),
)

add_to_builtins('utils.templateutils')