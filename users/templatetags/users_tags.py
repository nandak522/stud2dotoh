from django import template
from users.models import College, Company
from django.core.urlresolvers import reverse as url_reverse

register = template.Library()

@register.filter
def college_url(college_id):
    college_details = College.objects.filter(id=int(college_id)).values('id', 'slug', 'name')[0]
    return "<a href='%(url)s'>%(name)s</a>" % {'name':college_details['name'], 'url':url_reverse('users.views.view_college', args=(college_details['id'], college_details['slug']))}

@register.filter
def workplace_url(company_id):
    company_details = Company.objects.filter(id=int(company_id)).values('id', 'slug', 'name')[0]
    return "<a href='%(url)s'>%(name)s</a>" % {'name':company_details['name'], 'url':url_reverse('users.views.view_company', args=(company_details['id'], company_details['slug']))}  