from Quizzer.models.Base import QuizResultBase
from Profile.models import Profile
from Quizzer.models.Quiz import Quiz, QuizTtl
import random
from utils import displayInConsole


class QuizResult(QuizResultBase):
    @staticmethod
    def get(userCurrent, quizCurrentID, typeGiven='seq'):
        displayInConsole('QuizResult', True)

        profile = Profile.get(userCurrent)
        quizCurrent = Quiz.get(quizCurrentID)

        try:
            process = QuizResult.objects.filter(
                profile__user__id=(
                    None if userCurrent.is_anonymous else userCurrent.id
                ),
                quiz__id=quizCurrentID,
                type=typeGiven
            ).latest()

            if process.complete:
                raise Exception('Complete')
            return process

        except Exception:
            return QuizResult.createProcess(profile, quizCurrent, typeGiven)

    @staticmethod
    def getFirstQuestion(profileCurrent, quizCurrent, quizTotalResult,  # @UnusedVariable
                         typeGiven='seq'):
        displayInConsole('QuizResult', True)

        if typeGiven == 'seq':
            return quizCurrent.getFirstQuestion()
        elif typeGiven == 'rng':
            return quizCurrent.getRandomQuestion()
        elif typeGiven == 'pri':
            if quizTotalResult.areAnswersAccounted():
                return quizTotalResult.getFirstQuestion()
            else:
                return quizCurrent.getFirstQuestion()
        elif typeGiven == 'prirng':
            if quizTotalResult.areAnswersAccounted():
                quizTotalResult.setAnswersRange()
                return quizTotalResult.getRandomQuestion()
            else:
                return quizCurrent.getFirstQuestion()

    @staticmethod
    def createProcess(profileCurrent, quizCurrent, typeGiven='seq'):
        displayInConsole('QuizResult', True)

        quizTtl, resultBool = QuizTtl.objects.get_or_create(  # @UnusedVariable
            profile=profileCurrent,
            quiz=quizCurrent
        )
        curQ = QuizResult.getFirstQuestion(
            profileCurrent,
            quizCurrent,
            quizTtl,
            typeGiven
        )

        return QuizResult.objects.create(
            profile=profileCurrent,
            quiz=quizCurrent,
            type=typeGiven,
            quiz_total_result=quizTtl,
            current_question=curQ
        )

    def findPriorityQuestion(self):
        displayInConsole(self)

        for answerTotal in self.quiz_total_result.getAnswerResults():
            try:
                return self.choices.get(id=answerTotal.question.id)
            except:
                continue

    def getPriorityQuestion(self):
        displayInConsole(self)

        if self.quiz_total_result.areAnswersAccounted():
            return self.findPriorityQuestion()
        else:
            return self.quiz.getNextQuestion(self.current_question)

    def getRNGPriorityQuestion(self):
        displayInConsole(self)

        fitsInRange = False
        while not fitsInRange:
            numInRange = random.randint(0, self.getRangeMax())
            for choice in self.choices:
                choiceTotalResult = self.getAnswerTtl().get(question=choice)
                if QuizTtl.isNumInAnswerRange(choiceTotalResult, numInRange):
                    return choice

    def nextQuestion(self):
        displayInConsole(self)

        if self.type == 'seq':
            self.current_question = self.quiz.getNextQuestion(
                self.current_question
            )
        elif self.type == 'rng':
            self.current_question = random.choice(self.choices)
        elif self.type == 'pri':
            self.current_question = self.getPriorityQuestion()
        elif self.type == 'prirng':
            self.current_question = self.getRNGPriorityQuestion()

        self.save()

    def getQuestionChoices(self):
        displayInConsole(self)

        quizQuestions = self.quiz.getQAs()
        takenQuestions = self.answerresult_set.values_list('question__id')
        return quizQuestions.exclude(id__in=takenQuestions)

    def isChoice(self):
        displayInConsole(self)

        choices = self.getQuestionChoices()

        if choices.count() != 0:
            self.choices = choices
            return False
        else:
            return True

    def isLastQuestion(self):
        displayInConsole(self)

        if self.type == 'seq':
            return self.quiz.isLastQuestion(self.current_question)
        else:
            return self.isChoice()

    def update(self):
        displayInConsole(self)

        if not self.isLastQuestion():
            self.nextQuestion()
        else:
            self.complete = True
            self.save()
