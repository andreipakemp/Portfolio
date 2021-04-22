from django import forms
from django.forms import ModelForm
from Profile.models import FriendRequest
from utils import displayInConsole


class FormFriendRequest(ModelForm):
    
    def getNotRequestedUsers(self, user, queryset):
        displayInConsole(self)
        
        requested_users = FriendRequest.getRequestedUsers(user)
        return queryset.exclude(id__in=requested_users)        
    
    def getAvailUsers(self, user):
        displayInConsole(self)
        
        queryset = self.fields['to_user'].queryset.exclude(id=user.id)
        queryset = self.getNotRequestedUsers(user, queryset)
        self.fields['to_user'].queryset = queryset
    
    def __init__(self, *args, **kwargs):
        displayInConsole(self) 
               
        user = kwargs.pop('user')
        super(FormFriendRequest, self).__init__(*args, **kwargs)
        self.getAvailUsers(user)
    
    class Meta:
        model = FriendRequest
        exclude = ['from_user',]
        
class FormFriendDecision(ModelForm):
    
    requests = forms.ModelMultipleChoiceField(
        queryset = FriendRequest.objects.all(),
        widget  = forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = FriendRequest
        exclude = ['to_user', 'from_user']
        
    def setRequestFields(self, user):
        displayInConsole(self)
        
        self.fields['requests'].queryset = FriendRequest.getUsersRequests(user)   
#    
    def __init__(self, user, *args, **kwargs): 
        displayInConsole(self)
        
        super(FormFriendDecision, self).__init__(*args, **kwargs)
        self.setRequestFields(user)

    def hasRequests(self):
        displayInConsole(self)
        
        if self.fields['requests'].queryset.count() > 0:
            return True
        else:
            return False


