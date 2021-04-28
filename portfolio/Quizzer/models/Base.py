from django.db import models
from Base.models import CustomUser
from Profile.models import Profile
from utils import displayInConsole

class QuizBase(models.Model):
    PUBLIC = 'pub'
    PRIVATE = 'pri'
    FRIENDS = 'fri'
    
    SCOPE = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (FRIENDS, 'Friends'),
        ]
    
    name = models.CharField(
        'Quiz Name', 
        max_length=256
        )
    owner = models.ForeignKey(
        CustomUser,  
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL
        )
    visible_to = models.CharField(
        'Visible To', 
        max_length=3, 
        choices=SCOPE, 
        default=PUBLIC
        )
    modified_by = models.CharField(
        'Modified By', 
        max_length=3, 
        choices=SCOPE, 
        default=PUBLIC
        )
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name
    
class QA(models.Model):
    quiz = models.ForeignKey(
        'Quiz', 
        blank=False, 
        null=False, 
        on_delete=models.CASCADE
        )
    number = models.IntegerField(default=0)
    question = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)   
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return str(self.id)
    
class QuizTtlBase(models.Model):
    profile = models.ForeignKey(
        Profile,
        blank=False, 
        null=True, 
        on_delete=models.CASCADE        
        )        
    quiz = models.ForeignKey(
        'Quiz',
        blank=False, 
        null=False, 
        on_delete=models.CASCADE  
        )
    range_max = models.IntegerField(
        default = 0
        )
    
    class Meta:
        abstract = True
        
    
class QuizResultBase(models.Model):
    date = models.DateTimeField(
        auto_now_add=True,
        blank=True
        )
    profile = models.ForeignKey(
        Profile,
        blank=True, 
        null=True, 
        on_delete=models.CASCADE        
        )    
    quiz = models.ForeignKey(
        'Quiz',
        blank=False, 
        null=False, 
        on_delete = models.CASCADE  
        )
    type = models.CharField(
        max_length=6, 
        default='seq'
        )
    current_question = models.ForeignKey(
        QA, 
        on_delete = models.CASCADE  
        )
    complete = models.BooleanField(
        default=False
        )
    quiz_total_result = models.ForeignKey(
        'QuizTtl', 
        on_delete = models.CASCADE  
        )
    
    class Meta:
        get_latest_by = 'date'
        abstract = True
        
    def getAnswerTtl(self):
        displayInConsole(self)
        
        return self.quiz_total_result.answerttl_set
    
    def getRangeMax(self):
        displayInConsole(self)
        
        return self.quiz_total_result.range_max  
    
class AnswerResultBase(models.Model):
    quiz_process = models.ForeignKey(
        'QuizResult',
        blank=False, 
        null=False, 
        on_delete=models.CASCADE 
        )
    question = models.ForeignKey(
        QA,
        blank=False,         
        null=False, 
        on_delete=models.CASCADE 
        )
    result = models.BooleanField()
    
    class Meta:
        abstract = True
    
class AnswerTtlBase(models.Model):
    quiz_total_result = models.ForeignKey(
        'QuizTtl',        
        blank=False, 
        null=False, 
        on_delete=models.CASCADE
        )
    question = models.ForeignKey(
        QA,        
        blank=False, 
        null=False, 
        on_delete=models.CASCADE
        )
    weight = models.IntegerField(default=0)
    rangeMin = models.IntegerField(default=0)
    rangeMax = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-weight']
        abstract = True