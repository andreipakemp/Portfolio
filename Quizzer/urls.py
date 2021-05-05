from django.urls import path
from . import views
from Quizzer.views import ViewQuizCreate, ViewQuizList, ViewQuizDetail
from Quizzer.views.viewsQuiz import ViewQuiz, ViewQuizResult, ViewQuizTotal

#from Quizzer.views.viewsQuestions import ViewQuestionBase
#from Quizzer.views.viewsQuiz import ViewQuizStart#, ViewQuizResult

app_name = 'quizzer'

urlpatterns = [
    path('', views.main, name='main'),
    path('create_quiz/', ViewQuizCreate.as_view(), name='quiz-form'),    
    path('list_quizzes/', ViewQuizList.as_view(), name='quiz-list'),
    path('list_quizzes/<int:pk>/', ViewQuizDetail.as_view(), name='quiz-detail'),
    path('quiz/<str:type>/<int:id>/', ViewQuiz.as_view(), name='quiz'),
    path('quiz/<int:id>/result/', ViewQuizResult.as_view(), name='quiz-result'),
    path('quiz_total/<int:id>/', ViewQuizTotal.as_view(), name='quiz-total')
    
]