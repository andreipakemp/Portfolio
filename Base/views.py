from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request, 'index.html', {'title': "Andrei Pak's Portfolio"})

def otherPage(request):
    return render(request, 'other.html', {'title': "Other"})

class ViewUserCreate(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


#    