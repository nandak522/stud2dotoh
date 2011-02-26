from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404
from utils import get_data
from django.conf import settings

def anonymoususer(the_function):
    def _anonymoususer(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_homepage'))
        kwargs['next'] = get_data(request).get('next', '')
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