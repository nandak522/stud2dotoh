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

@login_required
def view_ask_question(request, question_template):
    raise NotImplementedError

@login_required
def view_questions(request, question_template):
    raise NotImplementedError