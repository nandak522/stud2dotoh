from django import template
import re

register = template.Library()

@register.filter
def emailify(email):
    return " at ".join(email.split('@'))

@register.filter
def domainify(domain):
    if not re.match(r'http://', domain):
        return "".join(['http://', domain])
    return domain