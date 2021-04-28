from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse
from Quizzer.forms.forms import FormQuiz
from Quizzer.models.Quiz import Quiz
from utils import displayInConsole

class ViewQuizCreate(CreateView):
    template_name = 'Quizzer/forms/quiz_form.html' 
    form_class = FormQuiz
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Quiz'
        return context
    
    def form_valid(self, form):
        displayInConsole(self)
        
        form.instance.owner_id = self.request.user.id
        return super(ViewQuizCreate, self).form_valid(form)
    
    def get_success_url(self):
        displayInConsole(self)
        
        return reverse('quizzer:quiz-list')

class ViewQuizList(ListView):
    model = Quiz
    context_object_name = 'all_quizes'
    
    def listAvailItems(self):
        displayInConsole(self)
        
        visibleItems = []
        
        for item in ListView.get_queryset(self):
            if item.isAvailableFor(self.request.user, 'visibility'):
                visibleItems.append(item.id)
        
        return visibleItems
    
    def get_queryset(self):
        displayInConsole(self)
        
        lst = ListView.get_queryset(self)
        return lst.filter(id__in=self.listAvailItems())
    
    def get_context_data(self, **kwargs):
        displayInConsole(self)
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quiz List'
        
        if self.request.session.get('redirect_msg'):
            context['msg'] = self.request.session['redirect_msg']
            self.request.session['redirect_msg'] = None
        return context        
    