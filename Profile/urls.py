from django.urls import path
from Profile.views import ViewFriendRequest, ViewFriendRequestState, ViewProfile
from django.urls.conf import re_path
#from django.urls.conf import re_path

app_name = 'profile'

urlpatterns = [
    re_path(r'^$|(?P<id>\d?)', ViewProfile.as_view(), name='profile'),
    path('friend_request/', ViewFriendRequest.as_view(), name='friend-request'),
    path('friend_request_list/', ViewFriendRequestState.as_view(), name='friend-request-list'),
#    re_path(r'^friend_request_list(?:/(?P<pk>[0-9]+))?/$', ViewFriendRequestList.as_view(), name='friend-request-list'),
    ]