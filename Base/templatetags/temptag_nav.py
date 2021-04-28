from django import template
from Profile.models import Profile
from utils import displayInConsole

register = template.Library()

@register.simple_tag
def curPathID(request, target): 
    displayInConsole('', True)  
        
    if request.path == target:
        return 'curPage'
    else:
        return 'othPage'    
    
@register.simple_tag
def checkProfile(request):  
    displayInConsole('', True)  
    
    if 'profile_id' not in request.session:
        request.session['profile_id'] = Profile.objects.create(user = None).id
    
#    print('[CONSOLE REPORT]Current Session Profile ID:' + str(request.session['profile_id']))
    return ''
#        
        