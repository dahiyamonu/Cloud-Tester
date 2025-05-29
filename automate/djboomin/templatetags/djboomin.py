from django import template
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from django.conf import settings

import re

register = template.Library()

@register.filter
def remscores(value):
    return value.replace('_', ' ')

@register.filter
def clean_output(value):
    if strip_tags(value) == 'True':
        return mark_safe('<td><img src="%sadmin/img/icon-yes.svg" alt="True"></td>' % (settings.STATIC_URL))
    elif strip_tags(value) == 'False':
        return mark_safe('<td><img src="%sadmin/img/icon-no.svg" alt="False"></td>' % (settings.STATIC_URL))
    else:
        return value

@register.simple_tag
def active(request, pattern, response_class='active'):
    import re

    pattern = pattern.replace('^', "^%s" % reverse('admin:index'))

    if re.search(pattern, request.path):
        return response_class

    pattern = pattern.replace(' ', "_")
    if re.search(pattern, request.path):
        return response_class

    return ''
