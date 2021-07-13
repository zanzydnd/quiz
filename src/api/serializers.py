from rest_framework import serializers

from api.models import Quiz, Question, QuestionAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ("id", "text", "is_right")


class QuestionSerializer(serializers.ModelSerializer):
    answer = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "text", "type", "answer")


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ("id", "name", "start_date", "end_date", "description", "questions")
        read_only_fields = ("start_date",)
