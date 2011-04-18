from django import template
from users.models import College, Company
from users.models import UserProfile
from django.core.urlresolvers import reverse as url_reverse
from django.template.defaultfilters import capfirst
from utils.templateutils import domain

register = template.Library()

@register.filter
def college_url(college_id):
    if not college_id:
        return ''
    college_details = College.objects.filter(id=int(college_id)).values('id', 'slug', 'name')[0]
    return "<a href='%(domain)s%(url)s'>%(name)s</a>" % {'domain':domain,
                                                          'name':capfirst(college_details['name']),
                                                          'url':url_reverse('users.views.view_college',
                                                                            args=(college_details['id'],
                                                                                  college_details['slug']))}

@register.filter
def workplace_url(workplace):
    if not workplace:
        return ''
    if isinstance(workplace, Company):
        workplace_type = 'company'
    else:
        workplace_type = 'college'
    workplace_id = workplace.id
    workplace_info = {'company':Company, 'college':College}
    workplace_details = workplace_info[workplace_type].objects.filter(id=int(workplace_id)).values('id', 'slug', 'name')[0]
    return "<a href='%(domain)s%(url)s'>%(name)s</a>" % {'domain':domain,
                                                          'name':capfirst(workplace_details['name']),
                                                          'url':url_reverse('users.views.view_company',
                                                                            args=(workplace_details['id'],
                                                                                  workplace_details['slug']))}

@register.inclusion_tag('domain_url.html')
def render_user_domain(userprofile):
    if userprofile:
        if isinstance(userprofile, dict):
            user_id = userprofile.get('id')
            slug = userprofile.get('slug')
            userprofile = UserProfile.objects.get(id=user_id, slug=slug)
        elif isinstance(userprofile, tuple):
            user_id = userprofile[0]
            slug = userprofile[1]
            userprofile = UserProfile.objects.get(id=user_id, slug=slug)
    if userprofile.is_domain_enabled:
        return {'domain_or_name': "<a class='profile_link' href='%(url)s'>%(name)s</a>" % {'name':userprofile.name, 'url':url_reverse('users.views.view_userprofile', args=(userprofile.slug,))}}
    return {'domain_or_name': userprofile.name}