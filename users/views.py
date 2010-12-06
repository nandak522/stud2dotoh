from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from users.models import UserProfile
from utils import response, post_data, loggedin_userprofile, slugify
from users.decorators import anonymoususer
from django.shortcuts import get_object_or_404
from django.contrib import messages
import os

@login_required
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
    public_uploaded_files = userprofile.public_uploaded_files
    return response(request, userprofile_template, {'userprofile': userprofile,
                                                    'public_uploaded_files': public_uploaded_files})

def view_homepage(request, homepage_template):
    return response(request, homepage_template, {})

def _create_directory_for_user(userprofile):
    user_directory_path = userprofile.user_directory_path
    if os.path.exists(user_directory_path):
        return user_directory_path
    os.mkdir(user_directory_path)
    return user_directory_path

def _convert_notes_to_file(content, filename, user_directory_path):
    filename = slugify(filename)
    supposed_filepath = "/".join([user_directory_path, filename])
    if settings.DOCSTORE_CONFIG['local']:
        if os.path.exists(supposed_filepath):
            supposed_filepath += '_1'
        file = open(supposed_filepath, 'w')
        file.write(content)
        file.close()
        return filename
    else:
        raise NotImplementedError

def _fetch_content_from_user_uploaded_file(userprofile, filename):
    user_directory_path = userprofile.user_directory_path
    if settings.DOCSTORE_CONFIG['local']:
        supposed_filepath = "/".join([user_directory_path, filename]) 
        if os.path.exists(supposed_filepath):
            file_content = open(supposed_filepath, 'r').read()
            return file_content
        #TODO:This should be file 404 and not any typical 404
        raise Http404
    raise NotImplementedError

@login_required
def view_notepad(request, notepad_template):
    from users.forms import SaveFileForm
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        public_uploaded_files = userprofile.public_uploaded_files
        return response(request, notepad_template, {'form':SaveFileForm(),
                                                    'public_uploaded_files':public_uploaded_files})
    form = SaveFileForm(post_data(request))
    userprofile = loggedin_userprofile(request)
    if form.is_valid():
        user_directory_path = _create_directory_for_user(userprofile)
        filename = _convert_notes_to_file(content=form.cleaned_data.get('content'),
                                          filename=form.cleaned_data.get('name'),
                                          user_directory_path=user_directory_path)
        from users.messages import SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE
        messages.success(request, SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE % filename)
        public_uploaded_files = userprofile.public_uploaded_files
        return response(request, notepad_template, {'public_uploaded_files':public_uploaded_files,
                                                    'form':SaveFileForm()})
    public_uploaded_files = userprofile.public_uploaded_files
    return response(request, notepad_template, {'public_uploaded_files':public_uploaded_files,
                                                'form':form})

@login_required
def view_notepad_preview(request, notepad_preview_template):
    raise NotImplementedError

@login_required
def view_file_content_view(request, filename):
    userprofile = loggedin_userprofile(request)
    file_content = _fetch_content_from_user_uploaded_file(userprofile, filename)
    return HttpResponse(content=file_content, mimetype='text/plain')

@login_required
def view_account_settings(request, settings_template):
    from users.forms import AccountSettingsForm
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        form = AccountSettingsForm({'name':userprofile.name,
                                    'slug':userprofile.slug})
        return response(request, settings_template, {'form':form})
    form = AccountSettingsForm(post_data(request))
    if form.is_valid():
        name = form.cleaned_data.get('name')
        slug = form.cleaned_data.get('slug')
        new_password = form.cleaned_data.get('new_password')
        userprofile.update(name=name, slug=slug, password=new_password)
        from users.messages import ACCOUNT_SETTINGS_SAVED
        messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, settings_template, {'form':form})  