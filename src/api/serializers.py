import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from api.models import Quiz, Question, QuestionAnswer, UserAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ("id", "text", "is_right")


class QuestionSerializer(serializers.ModelSerializer):
    answer = QuestionAnswerSerializer(many=True)

    def update(self, instance, validated_data):
        instance.text = validated_data['text']
        instance.type = validated_data['type']
        instance.save()
        return instance

    def create(self, validated_data):
        object = Question(text=validated_data['text'], type=validated_data['type'])
        object.save()
        for answ in validated_data['answer']:
            answer_object = QuestionAnswer(text=answ['text'], is_right=answ['is_right'], question=object)
            answer_object.save()
        if validated_data['quiz_id']:
            object.quiz.add(validated_data['quiz_id'])
            object.save()
        return object

    class Meta:
        model = Question
        fields = ("id", "text", "type", "answer")
        read_only_fields = ("answer",)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.end_date = validated_data['end_date']
        instance.description = validated_data['description']
        instance.save()
        return instance

    def create(self, validated_data):
        object = Quiz(name=validated_data['name'], end_date=validated_data['end_date'],
                      description=validated_data['description'])
        object.save()
        for dict in validated_data['questions']:
            question = QuestionSerializer().create(dict)
            object.questions.add(question)
        object.save()
        return object

    class Meta:
        model = Quiz
        fields = ("id", "name", "start_date", "end_date", "description", "questions")
        read_only_fields = ("start_date",)


class QuizSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("id", "name", "start_date", "end_date", "description")


class AnswerOnQuiz(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['text_question'] and attrs['text_question'].type != "TEXT":
            raise serializers.ValidationError("Isn't a text question")
        if attrs['text_question'] and attrs['chosen_answer']:
            raise serializers.ValidationError("You can't pick an answer for text type question.")
        if not attrs['text_question'] and not attrs['chosen_answer']:
            raise serializers.ValidationError("You can't send an empty answer")
        if attrs['chosen_answer']:
            if UserAnswer.objects.filter(
                    Q(user=attrs['user']) & Q(chosen_answer__question=attrs['chosen_answer'].question)) and attrs[
                'chosen_answer'].question.type != "MULTIPLE":
                raise serializers.ValidationError("You can't answer on single question twice.")
        return super().validate(attrs)

    class Meta:
        model = UserAnswer
        fields = ("user", "chosen_answer", "text", "text_question")


class QuestionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "text", "type")


class AnalysisQuizSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    questions = QuestionAnalysisSerializer(many=True)

    def get_answers(self, instance):
        user = self.context['request'].user
        list_ = []
        user_filter = Q(user=user)
        for question in instance.questions.all():
            query_filter = Q(text_question=question) | Q(chosen_answer__question=question)
            answers = UserAnswer.objects.filter(user_filter & query_filter)
            custom_map = {}
            custom_map["Question"] = question.text
            answers_str = []
            for answer in answers:
                if answer.text:
                    answers_str.append(answer.text)
                else:
                    answers_str.append(answer.chosen_answer.text)
            custom_map['user_answers'] = answers_str
            list_.append(custom_map)
        return list_

    class Meta:
        model = Quiz
        fields = (*QuizSerializer.Meta.fields, "answers")
