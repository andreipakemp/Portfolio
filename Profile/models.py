from django.db import models
from utils import displayInConsole

class Profile(models.Model):
    user = models.OneToOneField(
        to='Base.CustomUser', 
        on_delete=models.CASCADE, 
        null=True
        )
    friends = models.ManyToManyField(
        to='Base.CustomUser',
        related_name='friend', 
        blank=True, 
        )
    
    def __str__(self):
        if self.user:
            return self.user.username + ' profile'
        else:
            return 'Anonymous User'
        
    @staticmethod
    def get(user):
       if user.is_anonymous:
           return None
       else:
           return Profile.objects.get(user=user)
    
    @staticmethod    
    def getUserFriends(user):
        displayInConsole('Profile', True)
        
        return Profile.objects.get(
                user = user
                ).friends.all()
                
    @staticmethod
    def deleteProfile(profileID):
        displayInConsole('Profile', True)
        
        Profile.objects.get(id=profileID).delete()
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        to='Base.CustomUser', 
        related_name='from_user', 
        on_delete=models.CASCADE
        )
    to_user = models.ForeignKey(
        to='Base.CustomUser', 
        related_name='to_user', 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return 'friend request from ' + self.from_user.username + ' to ' + self.to_user.username

    @staticmethod
    def getRequestedUsers(user):
        displayInConsole('FriendRequest', True)

        query = FriendRequest.objects.filter(from_user=user)
        return query.values_list('to_user', flat=True)

    @staticmethod
    def getUsersRequests(user):
        displayInConsole('FriendRequest', True)
        
        return FriendRequest.objects.filter(to_user=user.id)
#            
#    