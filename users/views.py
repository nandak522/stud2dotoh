from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect
from users.models import UserProfile
from utils import response, post_data
from users.decorators import anonymoususer
from django.shortcuts import get_object_or_404
from django.contrib import messages

def view_all_users(request, all_users_template):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(UserProfile.objects.values('id', 'name', 'slug', 'user__username', 'created_on'), 2)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)
    return response(request, all_users_template, {'users': users})

@anonymoususer
def view_register(request, registration_template, next=''):
    from users.forms import UserSignupForm
    if request.method == 'POST':
        form = UserSignupForm(post_data(request))
        if form.is_valid():
            userprofile = _handle_user_registration(form)
            from users.messages import USER_SIGNUP_SUCCESSFUL
            messages.success(request, USER_SIGNUP_SUCCESSFUL)
            return _let_user_login(request,
                                   userprofile.user,
                                   username=form.cleaned_data.get('username'),
                                   password=form.cleaned_data.get('password'),
                                   next=form.cleaned_data.get('next'))
    else:
        form = UserSignupForm()
    return response(request, registration_template, {'form': form, 'next': next})

def _handle_user_registration(registration_form):
    return UserProfile.objects.create_userprofile(username=registration_form.cleaned_data.get('username'),
                                                 email=registration_form.cleaned_data.get('email'),
                                                 password=registration_form.cleaned_data.get('password'),
                                                 name=registration_form.cleaned_data.get('name'))

def _authenticate_user(user):
    raise NotImplementedError

def _let_user_login(request, user, username, password, next=''):
    user = django_authenticate(username=username, password=password)
    django_login(request, user)
    if next:
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_homepage'))

@anonymoususer
def view_login(request, login_template, next=''):
    from users.forms import UserLoginForm
    if request.method == 'POST':
        form = UserLoginForm(post_data(request))
        if form.is_valid():
            userprofile = UserProfile.objects.get(user__username=form.cleaned_data.get('username'))
            if not userprofile.check_password(form.cleaned_data.get('password')):
                from users.messages import USER_LOGIN_FAILURE
                messages.error(request, USER_LOGIN_FAILURE)
                return response(request, login_template, {'form': form, 'next': next})
            from users.messages import USER_LOGIN_SUCCESSFUL
            messages.success(request, USER_LOGIN_SUCCESSFUL)
            return _let_user_login(request,
                                   userprofile.user,
                                   username=form.cleaned_data.get('username'),
                                   password=form.cleaned_data.get('password'),
                                   next=form.cleaned_data.get('next'))
    else:
        form = UserLoginForm()
    return response(request, login_template, {'form': form, 'next': next})

def view_logout(request, logout_template):
    django_logout(request)
    from users.messages import USER_LOGOUT_SUCCESSFUL
    messages.info(request, USER_LOGOUT_SUCCESSFUL)
    return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_homepage'))

def view_userprofile(request, user_id, user_slug_name, userprofile_template):
    userprofile = get_object_or_404(UserProfile, id=int(user_id), slug=user_slug_name)
    return response(request, userprofile_template, {'userprofile': userprofile})

def view_homepage(request, homepage_template):
    return response(request, homepage_template, {})