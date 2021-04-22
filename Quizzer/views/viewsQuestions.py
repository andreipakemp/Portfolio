from django.views.generic.edit import FormView
from Quizzer.forms.forms import FormQuizA
from utils import displayInConsole

class ViewQuestionBase(FormView):
    form_class = FormQuizA
    template_name = 'Quizzer/q_and_a_detail.html'     
    
    def get_context_data(self, **kwargs):
        displayInConsole(self)
        
        context = super(ViewQuestionBase, self).get_context_data(**kwargs)
        context['title'] = 'Quiz Question'
        
        return context