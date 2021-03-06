from django.contrib.auth.forms import UserCreationForm
from Base.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 
            'email'
            )        
