from django import forms
from django.forms import ModelForm
from Quizzer.models.Quiz import Quiz
from Quizzer.models.Base import QA

class FormQuiz(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Quiz
        exclude = ['owner',]
        
class FormQuizQA(ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = QA
        exclude = ['quiz', 'number']
        
class FormQuizA(ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = QA
        fields = ['answer']
