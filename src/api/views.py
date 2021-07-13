import json
from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response

from api.models import Quiz, Question, UserAnswer
from api.serializers import QuizSerializer, QuestionSerializer, QuizSerializerForUser, AnswerOnQuiz, \
    AnalysisQuizSerializer, AuthSerializer

User = get_user_model()


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


@swagger_auto_schema(
    method="post",
    request_body=AuthSerializer,
    operation_summary="Authentication",
    responses={200: "authenticated"},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def authenticate_user(request):
    username = request.data['username']
    password = request.data['password']

    lg = authenticate(username=username, password=password)

    if lg is None:
        return Response(status=401)
    else:
        login(request, lg)
        return Response(status=200, data={200: "authenticated"})


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    """Опрос"""
    permission_classes = [IsAdminUser]
    queryset = Quiz.objects.filter(Q(start_date__lte=datetime.today()) & Q(end_date__gte=datetime.today()))

    def get_serializer_class(self):
        return QuizSerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_queryset(self):
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
