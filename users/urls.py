from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    (r'^$', 'view_all_users', {'all_users_template':'all_users.html'}, 'all_users'),
    (r'^(?P<user_slug_name>[\w\s-]+)/$', 'view_userprofile', {'userprofile_template':'user_profile.html'}, 'user_profile'),
    (r'^notes/(?P<note_id>\d+)/$', 'view_note', {}, 'show_note'),
    (r'^notes/(?P<note_id>\d+)/edit/$', 'view_edit_note', {'notepad_template':'notepad.html'}, 'edit_note'),
)
