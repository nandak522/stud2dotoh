from django.conf.urls.defaults import *
from django.conf import settings
from django.template import add_to_builtins

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^robots.txt$', 'django.views.generic.simple.direct_to_template', {
                'template': 'robots.txt' }),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    (r'^users/', include('users.urls')),
    (r'^questions/', include('quest.urls')),
    (r'^utils/', include('utils.urls')),
)

urlpatterns += patterns('users.views',
    (r'^$', 'view_homepage', {'homepage_template':'homepage.html'}, 'homepage'),
    (r'^dashboard/$', 'view_dashboard', {'dashboard_template':'dashboard.html'}, 'dashboard'),
    (r'^notepad/$', 'view_notepad', {'notepad_template':'notepad.html'}, 'notepad'),
    (r'^webresume/$', 'view_webresume', {}, 'webresume'),
    (r'^invite/$', 'view_invite', {'invite_template':'invite.html'}, 'invite'),
    (r'^achievements/$', 'view_all_achievements', {'achievements_template':'achievements.html'}, 'achievements'),
)

urlpatterns += patterns('users.views',
    (r'^accounts/register/$', 'view_register', {'registration_template': 'register.html'}, 'register'),
    (r'^accounts/studentregister/$', 'view_register', {'registration_template': 'student_register.html', 'user_type':'S'}, 'student_register'),
    (r'^accounts/employeeregister/$', 'view_register', {'registration_template': 'employee_register.html', 'user_type':'E'}, 'employee_register'),
    (r'^accounts/professorregister/$', 'view_register', {'registration_template': 'professor_register.html', 'user_type':'P'}, 'professor_register'),
    (r'^accounts/login/$', 'view_login', {'login_template': 'login.html'}, 'login'),
    (r'^accounts/logout/$', 'view_logout', {'logout_template': 'logout.html'}, 'logout'),
    (r'^contactuser/(?P<user_id>\d+)/$', 'view_contactuser', {'contactuser_template':'contactuser.html'}, 'contactuser'),
    (r'^contactgroup/(?P<group_type>\w+)/(?P<group_id>\d+)/$', 'view_contactgroup', {'contactgroup_template':'contactgroup.html'}, 'contactgroup'),
    (r'^contactus/$', 'view_contactus', {'contactus_template':'contactus.html'}, 'contactus'),
    (r'^forgot_password/$', 'view_forgot_password', {'forgot_password_template':'forgot_password.html'}, 'forgot_password'),
    (r'^reset_my_password/$', 'view_reset_my_password', {'reset_my_password_template':'reset_my_password.html'}, 'reset_my_password'),
    (r'^add_achievement/$', 'view_add_achievement', {'add_achievement_template':'add_or_edit_achievement.html'}, 'add_achievement'),
    (r'^edit_achievement/(?P<achievement_id>\d+)/$', 'view_edit_achievement', {'edit_achievement_template':'add_or_edit_achievement.html'}, 'edit_achievement'),
)

urlpatterns += patterns('users.views',
    (r'^settings/$', 'view_account_settings', {'settings_template':'settings.html'}, 'settings'),
    (r'^settings/personal/$', 'view_save_personal_settings', {'personal_settings_template':'personal_settings.html'}, 'personal_settings'),
    (r'^settings/acad/$', 'view_save_acad_settings', {'acad_settings_template':'acad_settings.html'}, 'acad_settings'),
    (r'^settings/workinfo/$', 'view_save_workinfo_settings', {'workinfo_settings_template':'workinfo_settings.html'}, 'workinfo_settings'),                    
)

urlpatterns += patterns('users.views',
    (r'^colleges/$', 'view_colleges', {'colleges_template':'colleges.html'}, 'colleges'),
    (r'^colleges/(?P<college_id>\d+)/(?P<college_slug>[\w\s-]+)/$', 'view_college', {'college_template':'college.html'}, 'college_profile'),
)

urlpatterns += patterns('users.views',
    (r'^companies/$', 'view_all_companies', {'companies_template':'companies.html'}, 'companies'),
    (r'^companies/(?P<company_id>\d+)/(?P<company_slug>[\w\s-]+)/$', 'view_company', {'company_template':'company.html'}, 'company_profile'),
)

add_to_builtins('utils.templateutils')
