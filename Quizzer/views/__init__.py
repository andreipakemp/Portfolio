from django.shortcuts import render
from .views import *

def main(request):
    return render(request, 'main.html', {'title': "Quizzer Main"})