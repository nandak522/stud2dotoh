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
    (r'^accounts/studentregister/$', 'view_register', {'registration_template': 'student_register.html', 'user_type':'S'}, 'student_register'),
    (r'^accounts/employeeregister/$', 'view_register', {'registration_template': 'employee_register.html', 'user_type':'E'}, 'employee_register'),
    (r'^accounts/professorregister/$', 'view_register', {'registration_template': 'professor_register.html', 'user_type':'P'}, 'professor_register'),
    (r'^accounts/login/$', 'view_login', {'login_template': 'login.html'}, 'login'),
    (r'^accounts/logout/$', 'view_logout', {'logout_template': 'logout.html'}, 'logout'),
    (r'^settings/$', 'view_account_settings', {'settings_template':'settings.html'}, 'settings'),
    (r'^settings/personal/$', 'view_save_personal_settings', {'personal_settings_template':'personal_settings.html'}, 'personal_settings'),
    (r'^settings/acad/$', 'view_save_acad_settings', {'acad_settings_template':'acad_settings.html'}, 'acad_settings'),
    (r'^settings/workinfo/$', 'view_save_workinfo_settings', {'workinfo_settings_template':'workinfo_settings.html'}, 'workinfo_settings'),
)

add_to_builtins('utils.templateutils')