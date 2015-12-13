from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def classes(value, arg):
    return value.as_widget(attrs={"class": arg})
