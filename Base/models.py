from django.contrib.auth.models import AbstractUser
from Profile.models import Profile
from utils import displayInConsole

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        displayInConsole(self)
                
        AbstractUser.save(self, *args, **kwargs)
        if 'update_fields' not in kwargs:
            Profile.objects.create(user=self)
    
