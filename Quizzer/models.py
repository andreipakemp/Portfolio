from django.db import models
from django.contrib.auth.models import User 

class Quiz(models.Model):
    PUBLIC = 'a'
    PRIVATE = 'b'
    FRIENDS = 'c'
    
    SCOPE = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (FRIENDS, 'Friends'),
        ]
    
    name = models.CharField('Quiz Name', max_length=256)
    owner = models.ForeignKey(
        User, 
        related_name='owner_name', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL
        )
    visibleTo = models.CharField('Visible To', max_length=1, choices=SCOPE, default=PUBLIC)
    modifiedBy = models.CharField('Modified By', max_length=1, choices=SCOPE, default=PUBLIC)
    
    def __str__(self):
        return self.name

class Q_And_A(models.Model):
    quiz = models.ForeignKey(
        Quiz, 
        related_name='QA', 
        blank=False, 
        null=False, 
        on_delete=models.CASCADE
        )
    question = models.CharField(max_length=256)
    answear = models.CharField(max_length=256)   
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return str(self.id)
    #self.quiz + ' question id:' + self.id