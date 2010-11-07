from django import template

register = template.Library()

@register.filter
def emailify(email):
    return " at ".join(email.split('@'))