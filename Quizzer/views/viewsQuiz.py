from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView
from Quizzer.forms.forms import FormQuizQA, FormQuizA
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse
from Quizzer.models.Quiz import Quiz, AnswerResult
from Quizzer.models.Base import QA
from Quizzer.models.QuizResultClass import QuizResult
from utils import displayInConsole
    
class ViewQuizDetail(View):
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quiz Detail'
        return context
    
    def get(self, request, *args, **kwargs):
        displayInConsole(self)
        
        view = ViewQuizInfo.as_view()
        return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        displayInConsole(self)
        
        view = ViewQuestionCreate.as_view()
        return view(request, *args, **kwargs)

class ViewQuizInfo(SingleObjectMixin, ListView):
    template_name = 'Quizzer/quiz_detail.html'
    paginate_by = 10    
    
    def get(self, request, *args, **kwargs):
        displayInConsole(self)
        
        self.object = self.get_object()         
        return super().get(request, *args, **kwargs)      
    
    def get_context_data(self, **kwargs):
        displayInConsole(self)
        
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.object
        context['title'] = 'Quiz Info'
        
        if self.object.isAvailableFor(self.request.user, 'modification'):
            context['form'] = FormQuizQA()
        return context
    
    def get_queryset(self):
        displayInConsole(self)
        
        return self.object.qa_set.all()
    
    def get_object(self, queryset=None):
        displayInConsole(self)   
             
        obj = SingleObjectMixin.get_object(self, queryset=Quiz.objects.all())
        
        if obj.isAvailableFor(self.request.user, 'visibility'):
            return obj
    
class ViewQuestionCreate(CreateView):
    
    form_class = FormQuizQA
    template_name = 'Quizzer/quiz_detail.html' 
    
    def get_context_data(self, **kwargs):
        displayInConsole(self) 
          
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Question'
        return context
    
    def get_success_url(self):
        displayInConsole(self)
        
        return reverse('quizzer:quiz-detail', kwargs={'pk': self.kwargs['pk']})
        
    def form_valid(self, form):
        displayInConsole(self)
        
        quizID = self.kwargs['pk']
        form.instance.quiz_id = quizID
        cur_quiz = Quiz.objects.get(id=quizID)
        questionCount = QA.objects.filter(quiz=cur_quiz).count()
        form.instance.number = questionCount + 1
        return super(ViewQuestionCreate, self).form_valid(form)

class ViewQuiz(FormView):
    form_class = FormQuizA
    template_name = 'Quizzer/q_and_a_detail.html'  
    
    @property
    def get_initial(self):
        displayInConsole(self)
        
        self.currentProcess = QuizResult.get(
            self.request.user, 
            self.kwargs['id'],
            self.kwargs['type']
            )
        self.quiz = Quiz.objects.get(id=self.kwargs['id'])
        self.QA = self.currentProcess.current_question
                
        return FormView.get_initial(self)
    
    def get_context_data(self, **kwargs):
        displayInConsole(self)
        
        context = FormView.get_context_data(self, **kwargs)
        context['title'] = 'Quiz'
        context['quiz'] = self.quiz
        context['question'] = self.QA.question
        return context
    
    def form_valid(self, form): 
        displayInConsole(self)   
            
        AnswerResult.create(
            self.currentProcess, 
            self.QA, 
            form.instance.answer
            )
            
        return FormView.form_valid(self, form)
    
    def get_success_url(self):
        displayInConsole(self)  
        
        if not self.currentProcess.complete:
            return reverse(
                'quizzer:quiz', 
                kwargs={
                    'type':self.kwargs['type'],
                    'id':self.kwargs['id']
                    }
                )
        else:
            return reverse(
                'quizzer:quiz-result',
                kwargs={
                    'type':self.kwargs['type'],
                    'id':self.kwargs['id']
                    }
                )
    
class ViewQuizTotal(DetailView):
    model = QuizResult
    context_object_name = 'process'
    
    def get_context_data(self, **kwargs):
        displayInConsole(self)

        # noinspection PyTypeChecker
        context = FormView.get_context_data(self, **kwargs)
        context['title'] = 'Quiz Total'
        return context
    
    def get_object(self):
        displayInConsole(self)
        
        self.object = QuizResult.objects.filter(
                profile__user__id = None if self.request.user.is_anonymous else self.request.user.id,
                quiz__id = self.kwargs['id'],
                type = self.kwargs['type']
                ).latest()
        return self.object