from django.contrib import admin
from Profile.models import Profile, FriendRequest
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(FriendRequest)

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user', 'show_friends')
    filter_horizontal = ['friends']
#    queryset = queryset.exclude(friends=)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'friends':
            kwargs['queryset'] = User.objects.exclude(id=request.user.id)
        return admin.ModelAdmin.formfield_for_manytomany(self, db_field, request, **kwargs)
    
    def show_friends(self, obj):
        return "\n".join([a.username+',' for a in obj.friends.all()])
