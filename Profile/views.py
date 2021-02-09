from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Profile.forms import FormFriendRequest, FormFriendDecision
from Profile.models import FriendRequest, Profile
from django.urls.base import reverse
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.list import ListView

@method_decorator(login_required, name='dispatch')
class ViewFriendRequest(CreateView):
    template_name = 'friend_request.html'
    form_class = FormFriendRequest    
     
    def get_form_kwargs(self):
        kwargs = super(ViewFriendRequest, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('msg'):
            context['msg'] = self.request.session['msg']
            self.request.session['msg'] = None
        return context
    
    def form_valid(self, form):
        new_obj = form.instance 
        new_obj.from_user = self.request.user
        try:
            FriendRequest.objects.get(
                from_user=new_obj.from_user,
                to_user=new_obj.to_user
            )            
            
        except FriendRequest.DoesNotExist:
            self.request.session['msg'] = 'Friend request sent'            
            return super().form_valid(form)
#        
        self.request.session['msg'] = 'Friend request already sent'
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('profile:friend-request')
    
@method_decorator(login_required, name='dispatch')
class ViewFriendRequestState(FormView):

    model = FriendRequest
    template_name = 'Profile/friendrequest_list.html'
        
    def get_form(self):
        form = FormFriendDecision(self.request.user)
        return form 
    
    def post(self, request, *args, **kwargs):

        current_request = FriendRequest.objects.get(id=request.POST['requests'])
        
        if 'approve' in request.POST:
            profile = Profile.objects.get(user=self.request.user)            
            new_friend = current_request.from_user
            profile.friends.add(new_friend)
        
        current_request.delete()      
        
        return FormView.post(self, request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ViewProfile(DetailView):
    model = Profile

    def get_object(self):
        while 'id' in self.request.GET:
            try:
                self.object = Profile.objects.get(user=self.request.GET['id'])
                return self.object
            except Profile.DoesNotExist:
                break

        self.object =Profile.objects.get(user=self.request.user)
        return self.object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.object.friends.all()
        return context

#class ViewProfile(SingleObjectMixin, ListView):
#    #model = Quiz
#    template_name = 'Profile/profile_detail.html'
#    paginate_by = 10
#    queryset = None 
##    object = None
#
#    def get_queryset(self):
#        while 'id' in self.request.GET:
#            try:
#                self.queryset = Profile.objects.get(user=self.request.GET['id']).friends.all()
#                return self.queryset
#            except Profile.DoesNotExist:
#                break
#        
#        self.queryset = Profile.objects.get(user=self.request.user).friends.all()
#        return self.queryset
#        
#    
#    def get_object(self, queryset=None):
#        
#        self.get_queryset()
#        print(self.queryset.values('username'))
#        return self.queryset
#    
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['profile'] = self.object
#        return context
#    
#    def get(self, request, *args, **kwargs):
#        self.object = self.get_object(request) 
#        return super().get(request, *args, **kwargs)

    
    