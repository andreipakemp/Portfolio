from django.urls import path, include
from . import views

from Quizzer.views import ViewQuizCreate, ViewQuizList, ViewQuizDetail
from Quizzer.forms import forms

app_name = 'quizzer'

urlpatterns = [
    path('', views.main, name='main'),
    path('create_quiz/', ViewQuizCreate.as_view(), name='quiz-form'),
    
    path('list_quizzes/', ViewQuizList.as_view(), name='quiz-list'),
    path('list_quizzes/<int:pk>/', ViewQuizDetail.as_view(), name='quiz-detail'),
    
]