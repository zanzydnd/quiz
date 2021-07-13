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


class QuestionForCreateQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id",)
        read_only_fields = ("id",)


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

    def create(self, validated_data):
        object = Quiz(name=validated_data['name'], end_date=validated_data['end_date'],
                      description=validated_data['description'])
        object.save()
        for que in validated_data['questions']:
            object.questions.add(que)
        return object
