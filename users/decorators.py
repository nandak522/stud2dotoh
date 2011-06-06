from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from utils import get_data, loggedin_userprofile
from users.models import UserProfile
from django.contrib import messages

def anonymoususer(the_function):
    def _anonymoususer(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_homepage'))
        next = get_data(request).get('next', '')
        if next:
            kwargs['next'] = next        
        return the_function(request, *args, **kwargs)
    return _anonymoususer

def is_admin(the_function):
    def _is_admin(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            for admin_info in settings.ADMINS:
                if admin_info[1] == user.email:
                    return the_function(request, *args, **kwargs)
        raise Http404
    return _is_admin

def is_domain_slug_picked(the_function):
    def _is_domain_slug_picked(request, *args, **kwargs):
        user_slug_name = kwargs['user_slug_name']
        userprofile = get_object_or_404(UserProfile, slug=user_slug_name)
        user = request.user
        if user.is_authenticated():
            if user.get_profile().id == userprofile.id:
                if userprofile.can_update_slug():
                    from users.messages import NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE
                    messages.error(request, NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE)
                    return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
                return the_function(request, *args, **kwargs)
        if userprofile.can_update_slug():
            raise Http404
        return the_function(request, *args, **kwargs)
    return _is_domain_slug_picked

def is_premium_user(the_function):
    def _is_premium_user(request, *args, **kwargs):
        userprofile = loggedin_userprofile(request)
        if userprofile.is_premium:
            return the_function(request, *args, **kwargs)
        if datetime(datetime.now()-userprofile.created_on).days > settings.FREE_PERIOD:
            from users.messages import NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE
            messages.error(request, NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE)
            return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
    return _is_premium_user
