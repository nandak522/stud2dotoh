from django import template
import re
import urlparse
from django.template.defaulttags import URLNode, url
from django.contrib.sites.models import Site
from django.conf import settings

register = template.Library()

if settings.DEBUG:
    domain = ''
else:
    domain = "http://%s" % Site.objects.get_current().domain

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
