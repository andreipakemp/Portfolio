from django.shortcuts import render
from .views import *
from .viewsQuestions import *
from .viewsQuiz import *

def main(request):
    return render(request, 'main.html', {'title': "Quizzer Main"})