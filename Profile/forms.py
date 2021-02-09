from django import forms
from django.forms import ModelForm, Form
from Profile.models import FriendRequest
from django.contrib.admin.filters import ChoicesFieldListFilter

class FormFriendRequest(ModelForm):
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(FormFriendRequest, self).__init__(*args, **kwargs)
        self.fields['to_user'].queryset = self.fields['to_user'].queryset.exclude(id=user.id)
    
    class Meta:
        model = FriendRequest
        exclude = ['from_user',]
        
class FormFriendDecision(ModelForm):  #forms.Form
    
    requests = forms.ModelMultipleChoiceField(
        queryset = FriendRequest.objects.all(), # not optional, use .all() if unsure
        widget  = forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = FriendRequest
        exclude = ['to_user', 'from_user']
#    
#    
    def __init__(self, user, *args, **kwargs): 
        super(FormFriendDecision, self).__init__(*args, **kwargs)
        self.fields['requests'].queryset = FriendRequest.objects.filter(to_user=user.id)


