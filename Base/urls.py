from django.urls import path, include
from Base import views
from Base.views import ViewUserCreate
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('other', views.otherPage, name='other'),
    path('register/', ViewUserCreate.as_view(), name='register'),
    path(
        'register/success/', 
        TemplateView.as_view(template_name="registration/success.html"), 
        name='register-success'
    ),
    path('', include('django.contrib.auth.urls')),
#    path(
#        'send_friend_request/<int:userID>/', 
#        send_friend_request, 
#        name='send-friend-request'
#        ),
#    path(
#        'accept_friend_request/<int:requestID>/', 
#        accept_friend_request, 
#        name='accept-friend-request'
##        ),
#    path('friend_request/', ViewFriendRequest.as_view(), name='friend-request'),
#    path('friend_approval/', ViewFriendApprove.as_view(), name='friend-approval'),
#    path('friend_approval/<int:pk>/', ViewFriendApprove.as_view(), name='friend-approval'),
    
]