from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import redirect
from Quizzer.forms import FormQuiz, FormQuizQA
from Quizzer.models import Quiz 


class ViewQuizCreate(CreateView):
    template_name = 'Quizzer/forms/quiz_form.html' 
    form_class = FormQuiz
    
    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super(ViewQuizCreate, self).form_valid(form)
    
    def get_success_url(self):
        #print(self.kwargs)
        return reverse('quizzer:quiz-list')

class ViewQuizList(ListView):
    model = Quiz
    context_object_name = 'all_quizes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('redirect_msg'):
            context['msg'] = self.request.session['redirect_msg']
            self.request.session['redirect_msg'] = None
        return context

    
class ViewQuizInfo(SingleObjectMixin, ListView):
    #model = Quiz
    template_name = 'Quizzer/quiz_detail.html'
    paginate_by = 10    
    
    def get(self, request, *args, **kwargs):
        self.object = self.getObject(request)   
        if self.object:
            return super().get(request, *args, **kwargs)
        else: 
            request.session['redirect_msg'] = 'Not Permitted'
            return redirect('quizzer:quiz-list')         
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.object
        context['form'] = FormQuizQA()
        return context
    
    def get_queryset(self):
        return self.object.QA.all()
    
    def getObject(self, request):
        user = request.user
        object = self.get_object(queryset=Quiz.objects.all())
        owner = object.owner
        
        if user == owner or object.visibleTo == 'a':
            return object
    
    
class ViewQuestionCreate(CreateView):
    #model = Quiz
    form_class = FormQuizQA
    template_name = 'Quizzer/quiz_detail.html' 
    quizID = lambda self : self.kwargs['pk']
    
    def get_success_url(self):
        return reverse('quizzer:quiz-detail', kwargs={'pk': self.quizID()})
        
    def form_valid(self, form):
        form.instance.quiz_id = self.quizID()
        return super(ViewQuestionCreate, self).form_valid(form)
    
class ViewQuizDetail(View):
    def get(self, request, *args, **kwargs):
        view = ViewQuizInfo.as_view()
        return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs) :
        view = ViewQuestionCreate.as_view()
        return view(request, *args, **kwargs)