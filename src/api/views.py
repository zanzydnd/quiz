import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response

from api.models import Quiz, Question, UserAnswer
from api.serializers import QuizSerializer, QuestionSerializer, QuizSerializerForUser, AnswerOnQuiz, \
    AnalysisQuizSerializer

User = get_user_model()


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    """Опрос"""
    queryset = Quiz.objects.filter(Q(start_date__lte=datetime.today()) & Q(end_date__gte=datetime.today()))

    def get_serializer_class(self):
        return QuizSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self):
        print(self.kwargs)
        if self.kwargs.get('nested_1_pk'):
            return Question.objects.filter(quiz=self.kwargs.get('nested_1_pk'))
        else:
            return super(QuizQuestionViewSet, self).get_queryset()

    def create(self, request, *args, **kwargs):
        validated_data = QuestionSerializer().validate(request.data)
        validated_data['quiz_id'] = self.kwargs.get("nested_1_pk")
        object = QuestionSerializer().create(validated_data)
        return Response(status=204)


class ListQuizForUserView(ListAPIView):
    queryset = Quiz.objects.filter(Q(start_date__lte=datetime.today()) & Q(end_date__gte=datetime.today()))
    serializer_class = QuizSerializerForUser


class RetrieveAnswerForQuiz(CreateAPIView):
    serializer_class = AnswerOnQuiz
    queryset = UserAnswer.objects.all()


class QuizAnalysis(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = AnalysisQuizSerializer

    def get(self, request, *args, **kwargs):
        request.user = User.objects.get(id=self.kwargs['user_id'])
        return super(QuizAnalysis, self).get(request, *args, **kwargs)
