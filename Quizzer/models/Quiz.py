from Profile.models import Profile
import random
from Quizzer.models.Base import QuizBase, QuizTtlBase, AnswerTtlBase, AnswerResultBase
from utils import displayInConsole

class Quiz(QuizBase):    
    
    def getAvailState(self, state):
        displayInConsole(self)
        
        if state == 'visibility':
            return self.visible_to
        elif state == 'modification': 
            return self.modified_by
        
    def getOwnersFriends(self):
        displayInConsole(self)
        
        if self.owner != None:
            self.ownersFriends = Profile.getUserFriends(self.owner)
            return True
        else:
            False
    
    def isOwnersFriend(self, user):
        displayInConsole(self)
        
        if self.getOwnersFriends():
            return True if user in self.ownersFriends else False
        else:
            return False
    
    def isAvailableFor(self, user, state): 
        displayInConsole(self)     
          
        availability = self.getAvailState(state)  
        
        if availability == 'pub':
            return True
        elif availability == 'pri':
            return False
        elif availability == 'fri':
            return self.isOwnersFriend(user)
        
    def getQAs(self):
        displayInConsole(self)
        
        return self.qa_set        
        
    def getFirstQuestion(self):
        displayInConsole(self)
        
        return self.getQAs().first()
    
    def getRandomQuestion(self):
        displayInConsole(self)
        
        return random.choice(self.getQAs().all())
        
    def isLastQuestion(self, currentQuestion):
        displayInConsole(self)
        
        return self.getQAs().last().number == currentQuestion.number
#        
    def getNextQuestion(self, currentQuestion):
        displayInConsole(self)
        
        return self.getQAs().get(number=currentQuestion.number+1)
    
    @staticmethod
    def get(givenID):
        displayInConsole('Quiz', True) 
        
        return Quiz.objects.get(id=givenID)
        
class QuizTtl(QuizTtlBase):
       
    def getAnswerResults(self):
        displayInConsole(self)
        
        return self.answerttl_set.all()
    
    def areAnswersAccounted(self):
        displayInConsole(self)
        
        answersAccounted = self.getAnswerResults().count()
        questionNum = self.quiz.getQAs().count()
        return answersAccounted == questionNum
    
    def getFirstQuestion(self):
        displayInConsole(self)
        
        return self.getAnswerResults().first().question
    
    def setAnswersRange(self):
        displayInConsole(self)
        
        curRange = 0
        
        for answerTotal in self.getAnswerResults():
            answerTotal.rangeMin = curRange
            curRange += answerTotal.weight
            answerTotal.rangeMax = curRange
            answerTotal.save()
        
        self.range_max = curRange
        self.save()
        
    @staticmethod    
    def isNumInAnswerRange(answerResult, number):
        displayInConsole('QuizTtl', True) 
        
        overMin = number >= answerResult.rangeMin 
        underMax = number <= answerResult.rangeMax
        return True if overMin and underMax else False
        
    def getAnswerInRange(self, number):
        displayInConsole(self)
        
        for answerTotal in self.getAnswerResults():
            if QuizTtl.isNumInAnswerRange(answerTotal, number): 
                return answerTotal.question
            
    def getRandomQuestion(self):
        displayInConsole(self)
        
        numInRange = random.randint(0, self.range_max)
        return self.getAnswerInRange(numInRange)  
    
class AnswerResult(AnswerResultBase):
    
    @staticmethod
    def create(process, qa, givenAnswer):
        displayInConsole('AnswerResult', True) 
        
        answerBool = qa.answer == givenAnswer
              
        AnswerResult.objects.create(
            quiz_process = process,
            question = qa,
            result = answerBool
            )
        
        AnswerTtl.create(
            process.quiz_total_result,
            qa,
            answerBool
            )
                
        process.update()

class AnswerTtl(AnswerTtlBase):
    
    def setInitWeight(self, answerBool):
        displayInConsole(self)
        
        self.weight = 1 if answerBool else 2         
        self.save()
        
    def manageWeight(self, answerBool):
        displayInConsole(self)
        
        if not answerBool:
            self.weight += 1
            self.save()
            
    def setWeight(self, resultAvail, answerBool):
        displayInConsole(self)
        
        if resultAvail:
            self.setInitWeight(answerBool)
        else:
            self.manageWeight(answerBool)
    
    @staticmethod
    def create(quizTotalResult, qa, answerBool):
        displayInConsole('AnswerTtl', True) 
        
        answerTotalResult, resultBool = AnswerTtl.objects.get_or_create(
            quiz_total_result = quizTotalResult,
            question = qa
            )
        
        answerTotalResult.setWeight(resultBool, answerBool)