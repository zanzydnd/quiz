from django.contrib import admin


from api.models import Quiz, Question, QuestionAnswer, UserAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(UserAnswer)
