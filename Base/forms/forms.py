from django import forms
from django.forms import ModelForm, Form
#from Base.models import Friend_Request
from django.contrib.auth import get_user_model
from _operator import concat
from django.forms.fields import ChoiceField


        
#class FormFriendApproval(ModelForm):
#    
#    def __init__(self, *args, **kwargs):        
#        user = kwargs.pop('user')
#        super(FormFriendApproval, self).__init__(*args, **kwargs)
##        self.fields['to_user'].queryset = self.fields['to_user'].queryset.filter(id=user.id)
#    
#    class Meta:
#        model = Friend_Request
#        exclude = ['to_user']
        
