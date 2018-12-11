from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# Note the code for this is found at caktus group blog
#https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
@register.simple_tag(takes_context=True)
def url_page_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.filter
@stringfilter
def concatenate(str1, str2):
    """ concatenate str1 and str2"""
    return str(str1) + str(str2)
