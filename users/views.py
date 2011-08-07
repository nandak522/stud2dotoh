from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as url_reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from users.decorators import anonymoususer, is_admin, is_domain_slug_picked
from users.forms import ContactUserForm
from users.forms import PersonalSettingsForm, AcadSettingsForm, WorkInfoSettingsForm
from users.forms import StudentSignupForm, EmployeeSignupForm, ProfessorSignupForm
from users.forms import ContactUsForm, ContactGroupForm, InvitationForm, SaveNoteForm
from users.forms import ForgotPasswordForm, ResetMyPasswordForm, AddAchievementForm
from users.models import UserProfile, College, Company, Note, Achievement
from utils import response, post_data, loggedin_userprofile 
from utils.emailer import default_emailer, mail_admins, mail_group, invitation_emailer, welcome_emailer, forgot_password_emailer
from utils.decorators import is_get, is_post, is_ajax
from django.utils import simplejson
from taggit.models import Tag
from datetime import datetime

TODAY = datetime.today()
DEFAULT_COLLEGE_END_YEAR = TODAY.year + 1
DEFAULT_COLLEGE_START_YEAR = DEFAULT_COLLEGE_END_YEAR - 4

def view_homepage(request, homepage_template):
    #TODO:Homepage layout showing message, screenshots, latest updates across the system
    return response(request, homepage_template, {})

@login_required
@is_admin
def view_all_users(request, all_users_template):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(UserProfile.objects.values('id', 'name', 'slug', 'user__email', 'created_on'), settings.DEFAULT_PAGINATION_COUNT)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)
    return response(request, all_users_template, {'users': users})

def _get_signup_form_for_usertype(user_type):
    if user_type == 'S':
        form_to_be_loaded = StudentSignupForm
    elif user_type == 'P':
        form_to_be_loaded = ProfessorSignupForm
    elif user_type == 'E':
        form_to_be_loaded = EmployeeSignupForm
    return form_to_be_loaded

def _set_signup_greeting_for_usertype(request, user_type):
    if user_type == 'S':
        from users.messages import STUDENT_SIGNUP_GREETING
        messages.success(request, STUDENT_SIGNUP_GREETING)
    elif user_type == 'P':
        from users.messages import PROFESSOR_SIGNUP_GREETING
        messages.success(request, PROFESSOR_SIGNUP_GREETING)
    elif user_type == 'E':
        from users.messages import EMPLOYEE_SIGNUP_GREETING
        messages.success(request, EMPLOYEE_SIGNUP_GREETING)

@anonymoususer
def view_register(request, registration_template, user_type='', next=''):
    if not user_type:
        return response(request, registration_template, {'next':next})
    form_to_be_loaded = _get_signup_form_for_usertype(user_type)
    if request.method == 'GET':
        _set_signup_greeting_for_usertype(request, user_type)
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
        userprofile.join_college(college_name=registration_form.cleaned_data.get('college'))
    welcome_emailer(registration_form.cleaned_data.get('email'),
                    registration_form.cleaned_data.get('name'))
    return userprofile
        
def _let_user_login(request, user, email, password, next=''):
    user = django_authenticate(email=email, password=password)
    django_login(request, user)
    if next:
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseRedirect(redirect_to='/')

@anonymoususer
def view_login(request, login_template, next=''):
    from users.forms import UserLoginForm
    if request.method == 'POST':
        data = post_data(request)
        next = data.get('next') if not next else next 
        form = UserLoginForm(data)
        if form.is_valid():
            try:
                userprofile = UserProfile.objects.get(user__email=form.cleaned_data.get('email'), user__is_active=True)
            except UserProfile.DoesNotExist:
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
                                   next=next)
    else:
        form = UserLoginForm()
    return response(request, login_template, {'form': form, 'next': next})

def view_logout(request, logout_template):
    django_logout(request)
    from users.messages import USER_LOGOUT_SUCCESSFUL
    messages.info(request, USER_LOGOUT_SUCCESSFUL)
    return HttpResponseRedirect(redirect_to='/')

@is_domain_slug_picked
def view_userprofile(request, user_slug_name, userprofile_template):
    userprofile = get_object_or_404(UserProfile, slug=user_slug_name)
    public_notes = userprofile.public_notes
    asked_questions = userprofile.asked_questions
    answered_questions = userprofile.answered_questions
    achievements = userprofile.achievements
    can_edit = is_owner(request, userprofile)
    return response(request, userprofile_template, {'userprofile': userprofile,
                                                    'public_notes': public_notes,
                                                    'asked_questions':asked_questions,
                                                    'answered_questions':answered_questions,
                                                    'achievements':achievements,
                                                    'can_edit':can_edit})
@login_required
def view_notepad(request, notepad_template):
    userprofile = loggedin_userprofile(request)
    all_notes = userprofile.all_notes
    if request.method == 'GET':
        return response(request, notepad_template, {'form':SaveNoteForm(),
                                                    'all_notes':all_notes})
    form = SaveNoteForm(post_data(request))
    userprofile = loggedin_userprofile(request)
    if not form.is_valid():
        return response(request, notepad_template, {'form':form,
                                                    'all_notes':all_notes})
    Note.objects.create_note(userprofile=userprofile,
                             name=form.cleaned_data.get('name'),
                             short_description=form.cleaned_data.get('short_description'),
                             note=form.cleaned_data.get('content'),
                             public=form.cleaned_data.get('public'))
    from users.messages import SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE
    messages.success(request, SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE)
    return response(request, notepad_template, {'form':SaveNoteForm(),
                                                'all_notes':all_notes})

@login_required
def view_note(request, note_id):
    userprofile = loggedin_userprofile(request)
    note = get_object_or_404(Note, id=int(note_id))
    if userprofile.is_my_note(note):
        return HttpResponse(content=note.note, mimetype='text/plain')
    raise Http404

@login_required
def view_edit_note(request, note_id, notepad_template):
    userprofile = loggedin_userprofile(request)
    note = get_object_or_404(Note, id=int(note_id))
    if userprofile.is_my_note(note):
        all_notes = userprofile.all_notes
        if request.method == 'GET':
            form = SaveNoteForm({'name':note.name,
                                 'short_description':note.short_description,
                                 'content':note.note,
                                 'public':note.public})
            return response(request, notepad_template, {'form':form,
                                                        'note':note,
                                                        'all_notes':all_notes})
        form = SaveNoteForm(post_data(request))
        if form.is_valid():
            note.update(name=form.cleaned_data.get('name'),
                        short_description=form.cleaned_data.get('short_description'),
                        note=form.cleaned_data.get('content'),
                        public=form.cleaned_data.get('public'))
            from users.messages import SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE
            messages.success(request, SAVED_NOTEPAD_SUCCESSFULLY_MESSAGE)
        return response(request, notepad_template, {'form':SaveNoteForm(),
                                                    'all_notes':all_notes})
    raise Http404

@login_required
@is_get
def view_account_settings(request, settings_template):
    userprofile = loggedin_userprofile(request)
    personal_form = PersonalSettingsForm({'name':userprofile.name,
                                          'slug':userprofile.slug})
    (branch, college, start_year, end_year, aggregate) = userprofile.acad_details
    acad_form = AcadSettingsForm({'branch':branch,
                                  'college':college.name if college else '',
                                  'start_year':start_year if start_year else DEFAULT_COLLEGE_START_YEAR,
                                  'end_year':end_year if start_year else DEFAULT_COLLEGE_END_YEAR,
                                  'aggregate':aggregate if aggregate else ''})
    if userprofile.is_student:
        return response(request, settings_template, {'personal_form':personal_form,
                                                     'acad_form':acad_form})
    else:
        (workplace, designation, years_of_exp) = userprofile.work_details
        workinfo_form = WorkInfoSettingsForm({'workplace':workplace.name if workplace else '',
                                              'designation':designation,
                                              'years_of_exp':years_of_exp})
        return response(request, settings_template, {'personal_form':personal_form,
                                                     'acad_form':acad_form,
                                                     'workinfo_form':workinfo_form})

@login_required
@is_get
@is_ajax
def view_get_personal_settings(request, personal_settings_template):
    userprofile = loggedin_userprofile(request)
    form = PersonalSettingsForm({'name':userprofile.name,
                                 'slug':userprofile.slug,
                                 'new_password':''})
    return response(request, personal_settings_template, {'personal_form':form})

@login_required
@is_get
@is_ajax
def view_get_acad_settings(request, acad_settings_template):
    userprofile = loggedin_userprofile(request)
    (branch, college, start_year, end_year, aggregate) = userprofile.acad_details
    acad_form = AcadSettingsForm({'branch':branch,
                                  'college':college.name,
                                  'start_year':start_year,
                                  'end_year':end_year,
                                  'aggregate':aggregate})
    return response(request, acad_settings_template, {'acad_form':acad_form})

@login_required
@is_get
@is_ajax
def view_get_workinfo_settings(request, workinfo_settings_template):
    userprofile = loggedin_userprofile(request)
    (workplace, designation, years_of_exp) = userprofile.work_details
    form = WorkInfoSettingsForm({'workplace':workplace if workplace else '',
                                 'designation':designation,
                                 'years_of_exp':years_of_exp})
    return response(request, workinfo_settings_template, {'workinfo_form':form})

@login_required
@is_ajax
def view_save_personal_settings(request, personal_settings_template):
    if request.method == 'GET':
        return view_get_personal_settings(request, personal_settings_template)
    userprofile = loggedin_userprofile(request)
    form = PersonalSettingsForm(post_data(request))
    if form.is_valid():
        name = form.cleaned_data.get('name')
        new_password = form.cleaned_data.get('new_password')
        slug = form.cleaned_data.get('slug')
        if userprofile.can_update_slug():
            if slug:
                if UserProfile.objects.filter(slug=slug).count():
                    from users.messages import WEB_RESUME_URL_ALREADY_PICKED
                    form._errors['slug'] = WEB_RESUME_URL_ALREADY_PICKED
                else:
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
@is_post
@is_ajax
def view_save_acad_settings(request, acad_settings_template):
    if request.method == 'GET':
        return view_get_acad_settings(request, acad_settings_template)
    userprofile = loggedin_userprofile(request)
    acad_form = AcadSettingsForm(post_data(request))
    if acad_form.is_valid():
        branch = acad_form.cleaned_data.get('branch')
        college = acad_form.cleaned_data.get('college')
        start_year = acad_form.cleaned_data.get('start_year')
        end_year = acad_form.cleaned_data.get('end_year')
        aggregate = acad_form.cleaned_data.get('aggregate')
        userprofile.join_college(college_name=college,
                                 branch=branch,
                                 start_year=start_year,
                                 end_year=end_year,
                                 aggregate=aggregate)
        from users.messages import ACCOUNT_SETTINGS_SAVED
        messages.success(request, ACCOUNT_SETTINGS_SAVED)
    return response(request, acad_settings_template, {'acad_form':acad_form})

@login_required
@is_post
@is_ajax
def view_save_workinfo_settings(request, workinfo_settings_template):
    if request.method == 'GET':
        return view_get_workinfo_settings(request, workinfo_settings_template)
    userprofile = loggedin_userprofile(request)
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

def view_colleges(request, colleges_template):
    return response(request, colleges_template, {'colleges':College.objects.values('id', 'name', 'slug')})

def view_college(request, college_id, college_slug, college_template):
    college = get_object_or_404(College, id=int(college_id), slug=college_slug)
    return response(request, college_template, {'college':college, 'students':college.students})

def view_all_companies(request, companies_template):
    return response(request, companies_template, {'companies':Company.objects.values('id', 'name', 'slug')})

def view_company(request, company_id, company_slug, company_template):
    company = get_object_or_404(Company, id=int(company_id), slug=company_slug)
    return response(request, company_template, {'company':company, 'employees':company.employees})

@login_required
def view_contactuser(request, user_id, contactuser_template):
    userprofile = loggedin_userprofile(request)
    to_userprofile = get_object_or_404(UserProfile, id=int(user_id))
    if request.method == 'GET':
        return response(request, contactuser_template, {'contactuserform':ContactUserForm({'to':to_userprofile.name,
                                                                                           'message':'Hello,'}),
                                                        'to_userprofile':to_userprofile})
    form = ContactUserForm(post_data(request))
    if form.is_valid():
        try:
            default_emailer(from_email=userprofile.user.email,
                            to_emails=[form.cleaned_data.get('to')],
                            subject=form.cleaned_data.get('subject'),
                            message=form.cleaned_data.get('message'))
            from users.messages import CONTACTED_SUCCESSFULLY
            messages.success(request, CONTACTED_SUCCESSFULLY)
            return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_userprofile', args=(to_userprofile.slug,)))
        except Exception:
            from users.messages import CONTACTING_FAILED
            messages.error(request, CONTACTING_FAILED)
    return response(request, contactuser_template, {'contactuserform':form, 'to_userprofile':to_userprofile})

@login_required
def view_webresume(request):
    userprofile = loggedin_userprofile(request)
    if userprofile.can_update_slug():
        from users.messages import NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE
        messages.error(request, NEED_TO_PICK_A_WEBRESUME_URL_MESSAGE)
        return HttpResponseRedirect(url_reverse('users.views.view_account_settings'))
    return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_userprofile', args=(userprofile.slug,)))

@login_required
def view_contactgroup(request, group_type, group_id, contactgroup_template):
    userprofile = loggedin_userprofile(request)
    if group_type == 'college':
        group = get_object_or_404(College, id=int(group_id))
        to = "%s Students" % group.name
        redirect_url = url_reverse('users.views.view_college', args=(group_id, group.slug))
    elif group_type == 'company':
        group = get_object_or_404(Company, id=int(group_id))
        to = "%s Employees" % group.name
        redirect_url = url_reverse('users.views.view_company', args=(group_id, group.slug))
    else:
        raise Http404
    if request.method == 'POST':
        contactgroupform = ContactGroupForm(post_data(request))
        if contactgroupform.is_valid():
            mail_group(group_type=group_type,
                       group=group,
                       from_email=userprofile.user.email,
                       message=contactgroupform.cleaned_data.get('message'),
                       from_name=userprofile.name,
                       subject=contactgroupform.cleaned_data.get('subject'))
            from users.messages import CONTACTED_SUCCESSFULLY
            messages.success(request, CONTACTED_SUCCESSFULLY)
            return HttpResponseRedirect(redirect_to=redirect_url)
    contactgroupform = ContactGroupForm({'to':to})
    return response(request, contactgroup_template, {'contactgroupform':contactgroupform,
                                                     'group_type':group_type,
                                                     'group_id':group_id})

def view_contactus(request, contactus_template):
    if request.method == 'GET':
        return response(request, contactus_template, {'form':ContactUsForm()})
    form = ContactUsForm(post_data(request))
    if form.is_valid():
        mail_admins(from_email=form.cleaned_data.get('from_email'),
                    from_name=form.cleaned_data.get('from_name'),
                    subject=form.cleaned_data.get('subject'),
                    message=form.cleaned_data.get('message'))
        from users.messages import CONTACTED_SUCCESSFULLY
        messages.success(request, CONTACTED_SUCCESSFULLY)
        return HttpResponseRedirect(redirect_to='/')
    return response(request, contactus_template, {'form':form})

@login_required
def view_invite(request, invite_template):
    if request.method == 'GET':
        return response(request, invite_template, {'form':InvitationForm()})
    userprofile = loggedin_userprofile(request)
    form = InvitationForm(post_data(request))
    if form.is_valid():
        try:
            invitation_emailer(from_email=userprofile.user.email,
                               to_emails=form.cleaned_data.get('to_emails'),
                               from_name=userprofile.name)
            from users.messages import CONTACTED_SUCCESSFULLY
            messages.success(request, CONTACTED_SUCCESSFULLY)
            return HttpResponseRedirect(redirect_to='/')
        except Exception:
            from users.messages import CONTACTING_FAILED
            messages.error(request, CONTACTING_FAILED)
    return response(request, invite_template, {'form':form})

@anonymoususer
def view_forgot_password(request, forgot_password_template):
    if request.method == 'GET':
        form = ForgotPasswordForm()
        return response(request, forgot_password_template, {'form':form})
    form = ForgotPasswordForm(post_data(request))
    if not form.is_valid():
        return response(request, forgot_password_template, {'form':form})
    email = form.cleaned_data.get('email')
    try:
        from django.contrib.auth.models import get_hexdigest
        hash_key = get_hexdigest('md5', '', email)
        forgot_password_emailer(email, hash_key)
        from users.messages import SENT_FORGOT_PASSWORD_EMAIL_SUCCESSFULLY
        messages.success(request, SENT_FORGOT_PASSWORD_EMAIL_SUCCESSFULLY)
    except:
        from users.messages import CONTACTING_FAILED
        messages.error(request, CONTACTING_FAILED)
    return HttpResponseRedirect(redirect_to='/')

@anonymoususer
def view_reset_my_password(request, reset_my_password_template):
    if request.method == 'GET':
        if request.GET.has_key('email') and request.GET.has_key('hash_key'):
            email = request.GET.get('email')
            userprofile = get_object_or_404(UserProfile, user__email=email)
            retrieved_hash_key = request.GET.get('hash_key')
            from django.contrib.auth.models import get_hexdigest
            computed_hash_key = get_hexdigest('md5', '', email)
            if retrieved_hash_key == computed_hash_key:
                form = ResetMyPasswordForm()
                return response(request, reset_my_password_template, {'form':form,
                                                                      'email':email})
            from users.messages import INVALID_PASSWORD_RESET_HASH_KEY
            messages.error(request, INVALID_PASSWORD_RESET_HASH_KEY)
            return HttpResponseRedirect(redirect_to='/')
        else:
            raise Http404
    else:
        data = post_data(request)
        form = ResetMyPasswordForm(data)
        if form.is_valid():
            email = data.get('email')
            userprofile = get_object_or_404(UserProfile, user__email=email)
            password = form.cleaned_data.get('password')
            userprofile.set_password(password)
            from users.messages import PASSWORD_RESET_SUCCESSFULLY
            messages.success(request, PASSWORD_RESET_SUCCESSFULLY)
            return _let_user_login(request,
                                   userprofile.user,
                                   email=email,
                                   password=password)
        return response(request, reset_my_password_template, {'form':form,
                                                              'email':data.get('email')})

@login_required
def view_all_achievements(request, achievements_template):
    userprofile = loggedin_userprofile(request)
    achievements = userprofile.achievements
    return response(request, achievements_template, {'achievements':achievements})

@login_required
def view_add_achievement(request, add_achievement_template):
    userprofile = loggedin_userprofile(request)
    achievements = userprofile.achievements
    if request.method == 'GET':
        form = AddAchievementForm()
        return response(request, add_achievement_template, {'form':form,
                                                            'achievements':achievements})
    form = AddAchievementForm(post_data(request))
    if form.is_valid():
        Achievement.objects.create_achievement(userprofile,
                                               title=form.cleaned_data.get('title'),
                                               description=form.cleaned_data.get('description'))
        from users.messages import ACHIEVEMENT_ADDED_SUCCESSFULLY
        messages.success(request, ACHIEVEMENT_ADDED_SUCCESSFULLY)
        return HttpResponseRedirect(url_reverse('users.views.view_all_achievements'))
    return response(request, add_achievement_template, {'form':form,
                                                        'achievements':achievements})

@login_required
def view_edit_achievement(request, achievement_id, edit_achievement_template):
    userprofile = loggedin_userprofile(request)
    achievement = get_object_or_404(Achievement, id=int(achievement_id))
    if userprofile.is_my_achievement(achievement):
        achievements = list(userprofile.achievements)
        for achievment_info in achievements:
            if achievment_info['id'] == int(achievement_id):
                achievements.remove({'title':achievement.title,
                                        'id':int(achievement_id),
                                        'description':achievement.description})
                break
        if request.method == 'GET':
            form = AddAchievementForm({'title':achievement.title,
                                       'description':achievement.description})
            return response(request, edit_achievement_template, {'achievement':achievement,
                                                                 'form':form,
                                                                 'previous_achievements':achievements})
        form = AddAchievementForm(post_data(request))
        if form.is_valid():
            achievement.update(title=form.cleaned_data.get('title'),
                               description=form.cleaned_data.get('description'),)
            from users.messages import ACHIEVEMENT_UPDATED_SUCCESSFULLY
            messages.success(request, ACHIEVEMENT_UPDATED_SUCCESSFULLY)
            return HttpResponseRedirect(redirect_to=url_reverse('users.views.view_all_achievements'))
        return response(request, edit_achievement_template, {'achievement':achievement,
                                                             'form':form,
                                                             'previous_achievements':achievements})
    raise Http404
        
def is_owner(request, visitor_userprofile):
    '''If page you are visiting, like Web-Resume belongs to the same person
    who is currently logged in then return True else False '''
    user = request.user
    if user.is_authenticated():
       loggedin_userprofile = user.get_profile()
       if loggedin_userprofile.id == visitor_userprofile.id:
           return True
       return False
    else:
        return False
