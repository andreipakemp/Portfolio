from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.utils.decorators import method_decorator
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from Profile.forms import FormFriendRequest, FormFriendDecision
from Profile.models import FriendRequest, Profile
from Quizzer.models.Quiz import Quiz
from utils import displayInConsole, getSessionMsg

@method_decorator(login_required, name='dispatch')
class ViewFriendRequest(CreateView):
    template_name = 'friend_request.html'
    form_class = FormFriendRequest    
     
    def get_form_kwargs(self):
        displayInConsole(self)
        
        kwargs = super(ViewFriendRequest, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
        
    def get_context_data(self, **kwargs):
        displayInConsole(self)
        
        form = self.get_form()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Friend Request'
#        context['hasRequests'] = form.hasRequests()
        isMsg, msg = getSessionMsg(self) 
        if isMsg:
            context['msg'] = msg
            
        return context
    
    def requestExist(self, form):
        displayInConsole(self)
        
        new_obj = form.instance 
        new_obj.from_user = self.request.user
        
        try:
            FriendRequest.objects.get(
                from_user=new_obj.from_user,
                to_user=new_obj.to_user
            )            
            
        except FriendRequest.DoesNotExist:
            '''REQUEST SESSION GOTTA CHANGE'''
            self.request.session['msg'] = 'Friend request sent'            
            return True
#        
        self.request.session['msg'] = 'Friend request already sent'
        return False
    
    def form_valid(self, form):
        displayInConsole(self)
        
        if self.requestExist(form):
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    
    def get_success_url(self):
        displayInConsole(self)
        
        return reverse('profile:friend-request')
    
@method_decorator(login_required, name='dispatch')
class ViewFriendRequestState(FormView):

    model = FriendRequest
    template_name = 'Profile/friendrequest_list.html'
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'Friend Requests'
        return context
        
    def get_form(self):
        displayInConsole(self)
        
        form = FormFriendDecision(self.request.user)
        return form 
    
    def approveRequest(self, curRequest):
        displayInConsole(self)
        
        profile = Profile.objects.get(user=self.request.user)            
        new_friend = curRequest.from_user
        new_friend_profile = Profile.objects.get(user=new_friend)
        profile.friends.add(new_friend)
        new_friend_profile.friends.add(self.request.user)
        
    def handleRequest(self, request):
        displayInConsole(self)
        
        curRequest = FriendRequest.objects.get(id=request.POST['requests'])
        
        if 'approve' in request.POST:
            self.approveRequest(curRequest)
        
        curRequest.delete()
        
    def post(self, request, *args, **kwargs):
        displayInConsole(self)
        
        self.handleRequest(request)
        return FormView.post(self, request, *args, **kwargs)

class ViewProfile(DetailView):
    model = Profile

    def getProfile(self):
        if 'id' in self.kwargs:
            try:
                self.object = Profile.objects.get(user=self.kwargs['id'])
                return self.object
            except Profile.DoesNotExist:
                self.extra_context = {
                    'msg': 'Profile ID Does not Exist! Showing Your Profile instead.'
                }
                return

    def get_object(self):
        displayInConsole(self)
        
        self.getProfile()

        if not self.request.user.is_anonymous:
            self.object = Profile.objects.get(user=self.request.user)
            return self.object
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        
        if self.object:
            context['friends'] = self.object.friends.all()
            context['quizzes'] = Quiz.objects.filter(owner=self.object.user)
        else:
            context['msg'] = 'You must be logged in to view your profile!'
        return context

    
    