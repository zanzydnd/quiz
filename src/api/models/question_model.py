from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    TEXT_ANSWER_QUESTION = 'TEXT'
    SINGLE_ANSWER_QUESTION = 'SINGLE'
    MULTIPLE_ANSWER_QUESTION = 'MULTIPLE'
    TYPE_CHOICES = [
        (TEXT_ANSWER_QUESTION, 'TEXT'),
        (SINGLE_ANSWER_QUESTION, 'SINGLE'),
        (MULTIPLE_ANSWER_QUESTION, 'MULTIPLE')
    ]
    text = models.TextField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default=TEXT_ANSWER_QUESTION)

    class Meta:
        db_table = "question"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_right = models.BooleanField()

    class Meta:
        db_table = "question_answer"
        verbose_name = "Ответ для вопроса"
        verbose_name_plural = "Ответы для вопросов"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    text_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "user_answer"
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"