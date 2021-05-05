from django.contrib import admin
from Quizzer.models.Quiz import Quiz, QuizTtl, AnswerResult, AnswerTtl
from Quizzer.models.Base import QA
from Quizzer.models.QuizResultClass import QuizResult

class AdminDisplayID(admin.ModelAdmin):
    list_display = ('__str__', 'id')
    
class AdminAnswerNumber(AdminDisplayID):
    def get_list_display(self, request):
        return AdminDisplayID.list_display + ('question',)

admin.site.register(Quiz, AdminDisplayID)
admin.site.register(QA, AdminDisplayID)
admin.site.register(QuizResult, AdminDisplayID)
admin.site.register(AnswerResult, AdminAnswerNumber)
admin.site.register(QuizTtl, AdminDisplayID)
admin.site.register(AnswerTtl)

