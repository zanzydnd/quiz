from django.db import models

from .question_model import Question


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()
    description = models.TextField()
    questions = models.ManyToManyField(Question, related_name="quiz")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "quiz"
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
