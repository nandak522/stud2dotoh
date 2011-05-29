from django import template
import re
import urlparse
from django.template.defaulttags import URLNode, url
from django.contrib.sites.models import Site
from django.conf import settings
from datetime import datetime,time
from datetime import timedelta
from django.utils.dateformat import DateFormat 

register = template.Library()

domain = '' if settings.DEBUG else "http://%s" % Site.objects.get_current().domain

@register.filter
def emailify(email):
    return " at ".join(email.split('@'))

@register.filter
def domainify(domain):
    if not re.match(r'http://', domain):
        return "".join(['http://', domain])
    return domain

class AbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        return urlparse.urljoin(domain, path)

def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)
absurl = register.tag(absurl)

@register.filter
def humantime(t):
    #TODO:need to come up with strings like:
    #1)less than a minute ago
    #2)X minutes ago(if its less than an hour)
    #3)HH:MM a.m/p.m(if its on the same day)
    #4)DD/MM/YYYY, for everything else
    now = datetime.now()
    if datetime.combine(now, time()) < t and t < datetime.combine(now + timedelta(1), time()):
        f = 'g:i a'
    elif now.year == t.year:
        f = 'M j'
    else:
        f = 'n/j/y'
    df = DateFormat(t)
    return df.format(f).replace('.m.', 'm')
