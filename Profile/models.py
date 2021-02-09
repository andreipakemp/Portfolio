from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        User, 
        related_name='friend', 
        blank=True, 
        )
    
#    def __str__(self):
#        return self.user.username
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
#    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return 'friend request from ' + self.from_user.username + ' to ' + self.to_user.username
            
    