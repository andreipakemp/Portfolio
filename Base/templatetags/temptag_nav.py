from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from pickle import TRUE
from getpass import fallback_getpass


register = template.Library()

@register.simple_tag
def curPathID(request, target):     
    if request.path == target:
        return 'curPage'
    else:
        return 'othPage'    
