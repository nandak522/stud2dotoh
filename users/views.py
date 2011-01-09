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
from users.forms import PersonalSettingsForm, AcadSettingsForm, WorkInfoSettingsForm
from users.forms import StudentSignupForm, EmployeeSignupForm, ProfessorSignupForm

@login_required
def view_all_users(request, all_users_template):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(UserProfile.objects.values('id', 'name', 'slug', 'user__email', 'created_on'), 2)
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
def view_register(request, registration_template, user_type='', next=''):
    if not user_type:
        return response(request, registration_template, {'next':next})
    form_to_be_loaded = ''
    if user_type == 'S':
        form_to_be_loaded = StudentSignupForm
    elif user_type == 'P':
        form_to_be_loaded = ProfessorSignupForm
    elif user_type == 'E':
        form_to_be_loaded = EmployeeSignupForm
    if request.method == 'GET':
        return response(request, registration_template, {'form':form_to_be_loaded(), 'next':next})
    form = form_to_be_loaded(post_data(request))
    if form.is_valid():
        userprofile = _handle_user_registration(form, user_type=user_type)
        from users.messages import USER_SIGNUP_SUCCESSFUL
        messages.success(request, USER_SIGNUP_SUCCESSFUL)
        return _let_user_login(request,
                               userprofile.user,
                               email=form.cleaned_data.get('email'),
                               password=form.cleaned_data.get('password'),
                               next=form.cleaned_data.get('next'))
    return response(request, registration_template, {'form': form, 'next': next})

def _handle_user_registration(registration_form, user_type):
    userprofile = UserProfile.objects.create_profile(email=registration_form.cleaned_data.get('email'),
                                                     password=registration_form.cleaned_data.get('password'),
                                                     name=registration_form.cleaned_data.get('name'))
    if user_type == 'S':
        userprofile.make_student()
        userprofile.join_college(college_name=registration_form.cleaned_data.get('college'))
    elif user_type == 'P':
        userprofile.make_professor()
        userprofile.join_workplace(workplace_name=registration_form.cleaned_data.get('college'),
                                   workplace_type='College',
                                   designation='',
                                   years_of_exp=None)
    elif user_type == 'E':
        userprofile.make_employee()
        userprofile.join_workplace(workplace_name=registration_form.cleaned_data.get('company'),
                                   workplace_type='Company',
                                   designation='',
                                   years_of_exp=None)
    return userprofile
        
def _let_user_login(request, user, email, password, next=''):
    user = django_authenticate(email=email, password=password)
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
            try:
                userprofile = UserProfile.objects.get(user__email=form.cleaned_data.get('email'))
            except UserProfile.DoesNotExist:
                print 'Coming Here'
                from users.messages import USER_LOGIN_FAILURE
                messages.error(request, USER_LOGIN_FAILURE)
                return response(request, login_template, {'form': form, 'next': next})
            if not userprofile.check_password(form.cleaned_data.get('password')):
                from users.messages import USER_LOGIN_FAILURE
                messages.error(request, USER_LOGIN_FAILURE)
                return response(request, login_template, {'form': form, 'next': next})
            from users.messages import USER_LOGIN_SUCCESSFUL
            messages.success(request, USER_LOGIN_SUCCESSFUL)
            return _let_user_login(request,
                                   userprofile.user,
                                   email=form.cleaned_data.get('email'),
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
    asked_questions = userprofile.asked_questions
    answered_questions = userprofile.answered_questions
    #TODO: All Comments given
    return response(request, userprofile_template, {'userprofile': userprofile,
                                                    'public_uploaded_files': public_uploaded_files,
                                                    'asked_questions':asked_questions,
                                                    'answered_questions':answered_questions})

def view_homepage(request, homepage_template):
    #TODO:Homepage layout showing message, screenshots, latest updates across the system
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
    from users.forms import SaveNoteForm
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        public_uploaded_files = userprofile.public_uploaded_files
        return response(request, notepad_template, {'form':SaveNoteForm(),
                                                    'public_uploaded_files':public_uploaded_files})
    form = SaveNoteForm(post_data(request))
    userprofile = loggedin_userprofile(request)
    if form.is_valid():
        #TODO:If the notepad is made hidden, its not handled now
        user_directory_path = _create_directory_for_user(userprofile)
        filename = _convert_notes_to_file(content=form.cleaned_data.get('content'),
                                          filename=form.cleaned_data.get('name'),
                                          user_directory_path=user_directory_path)
        from users.messages import SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE
        messages.success(request, SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE % filename)
        public_uploaded_files = userprofile.public_uploaded_files
        return response(request, notepad_template, {'public_uploaded_files':public_uploaded_files,
                                                    'form':SaveNoteForm()})
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
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        personal_form = PersonalSettingsForm({'name':userprofile.name,
                                              'slug':userprofile.slug})
        (branch, college, start_year, end_year) = userprofile.acad_details
        acad_form = AcadSettingsForm({'branch':branch,
                                      'college':college.name if college else '',
                                      'start_year':start_year if start_year else 2007,#TODO:hardcoding year is not good
                                      'end_year':end_year if end_year else 2011})#TODO:hardcoding year is not good
        if userprofile.is_student:
            return response(request, settings_template, {'personal_form':personal_form,
                                                         'acad_form':acad_form})
        else:
            (workplace, designation, years_of_exp) = userprofile.work_details
            workinfo_form = WorkInfoSettingsForm({'workplace':workplace.name if workplace else '', 'designation':designation, 'years_of_exp':years_of_exp})
            return response(request, settings_template, {'personal_form':personal_form,
                                                         'acad_form':acad_form,
                                                         'workinfo_form':workinfo_form})
        
    form = PersonalSettingsForm(post_data(request))
    if form.is_valid():
        name = form.cleaned_data.get('name')
        slug = form.cleaned_data.get('slug')
        new_password = form.cleaned_data.get('new_password')
        userprofile.update(name=name, slug=slug, password=new_password)
        from users.messages import ACCOUNT_SETTINGS_SAVED
        messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, settings_template, {'form':form})  

@login_required
def view_save_personal_settings(request, personal_settings_template):
    if not request.is_ajax():#TODO:This has to go in a decorator
        return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        form = PersonalSettingsForm({'name':userprofile.name,
                                     'slug':userprofile.slug,
                                     'new_password':''})
        return response(request, personal_settings_template, {'personal_form':form})
    form = PersonalSettingsForm(post_data(request))
    if form.is_valid():
        name = form.cleaned_data.get('name')
        new_password = form.cleaned_data.get('new_password')
        slug = form.cleaned_data.get('slug')
        if userprofile.can_update_slug():
            if slug:
                userprofile.update(name=name, slug=slug, password=new_password)
                from users.messages import ACCOUNT_SETTINGS_SAVED
                messages.success(request, ACCOUNT_SETTINGS_SAVED)
            else:
                from users.messages import INVALID_WEB_RESUME_URL
                messages.error(request, INVALID_WEB_RESUME_URL)
        else:
            userprofile.update(name=name, password=new_password)
            from users.messages import ACCOUNT_SETTINGS_SAVED
            messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, personal_settings_template, {'personal_form':form})

@login_required
def view_save_acad_settings(request, acad_settings_template):
    if not request.is_ajax():#TODO:This has to go in a decorator
        return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        (branch, college, start_year, end_year) = userprofile.acad_details 
        acad_form = AcadSettingsForm({'branch':branch,
                                              'college':college.name,
                                              'start_year':start_year,
                                              'end_year':end_year})
        return response(request, acad_settings_template, {'acad_form':acad_form})
    acad_form = AcadSettingsForm(post_data(request))
    if acad_form.is_valid():
        branch = acad_form.cleaned_data.get('branch')
        college = acad_form.cleaned_data.get('college')
        start_year = acad_form.cleaned_data.get('start_year')
        end_year = acad_form.cleaned_data.get('end_year')
        userprofile.join_college(college_name=college, branch=branch, start_year=start_year, end_year=end_year)
        from users.messages import ACCOUNT_SETTINGS_SAVED
        messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, acad_settings_template, {'acad_form':acad_form})

@login_required
def view_save_workinfo_settings(request, workinfo_settings_template):
    if not request.is_ajax():#TODO:This has to go in a decorator
        return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
    userprofile = loggedin_userprofile(request)
    if request.method == 'GET':
        (workplace, designation, years_of_exp) = userprofile.work_details
        form = WorkInfoSettingsForm({'workplace':workplace if workplace else '',
                                     'designation':designation,
                                     'years_of_exp':years_of_exp})
        return response(request, workinfo_settings_template, {'workinfo_form':form})
    form = WorkInfoSettingsForm(post_data(request))
    if form.is_valid():
        workplace = form.cleaned_data.get('workplace')
        designation = form.cleaned_data.get('designation')
        years_of_exp = form.cleaned_data.get('years_of_exp')
        #TODO:Currently a Professor getting a corporate job is not handled
        if userprofile.is_student:
            workplace_type = 'Company'
            userprofile.make_employee()
        elif userprofile.is_employee:
            workplace_type = 'Company'
        else:
            workplace_type = 'College'
            userprofile.make_professor()
        userprofile.join_workplace(workplace, workplace_type, designation, years_of_exp)
        from users.messages import ACCOUNT_SETTINGS_SAVED
        messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, workinfo_settings_template, {'workinfo_form':form})