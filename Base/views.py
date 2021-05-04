from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from Base.forms.forms import CustomUserCreationForm
from Profile.models import Profile
from utils import displayInConsole

def index(request):    
    return render(
        request, 
        'index.html', 
        {'title': "Andrei Pak's Portfolio"}
        )

def otherPage(request):
    return render(
        request, 
        'other.html', 
        {'title': "Other"}
        )

def aboutPage(request):
    return render(
        request,
        'about.html',
        {'title': "About Me"}
        )

def projectsPage(request):
    return render(
        request,
        'projects.html',
        {'title': "My Projects"}
        )


class ViewUserCreate(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register-success')
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Registation'
        return context
    
    def form_valid(self, form):
        displayInConsole(self)
        form.save()
        return HttpResponseRedirect(self.success_url)
    
class ViewLoginCustom(LoginView):
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Login'
        return context
    
    def handleAnonUser(self):
        displayInConsole(self)
        
        if self.request.user.is_anonymous:
            profileID = self.request.session['profile_id']
            Profile.deleteProfile(profileID)
            
    def setSessionProfile(self, form):
        displayInConsole(self)
        
        self.request.session['profile_id'] = Profile.get(form.get_user()).id
    
    def form_valid(self, form):
        displayInConsole(self)
        
        self.handleAnonUser()
        self.setSessionProfile(form)           
        return LoginView.form_valid(self, form)
    
class ViewLogoutCustom(LogoutView):
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Logout'
        return context
    
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        displayInConsole(self)
        
        del request.session['profile_id']
        return LogoutView.dispatch(self, request, *args, **kwargs)
    



#    