from django import forms
from django.forms import ModelForm
from Quizzer.models import Q_And_A, Quiz 

class FormQuiz(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Quiz
        exclude = ['owner',]
        
class FormQuizQA(ModelForm):
    #required_css_class = 'required'
    class Meta:
        model = Q_And_A
        exclude = ['quiz']
