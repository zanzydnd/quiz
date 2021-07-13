from django.db import models

from .question_model import Question


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    description = models.TextField()
    questions = models.ManyToManyField(Question, related_name="quiz")

    class Meta:
        db_table = "quiz"
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
