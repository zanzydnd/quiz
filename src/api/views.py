from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Quiz
from api.serializers import QuizSerializer


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


class QuizViewSet(viewsets.ModelViewSet):
    """Опрос"""
    queryset = Quiz.objects.all()#filter(Q(start_date__lt=datetime.now()) & Q(end_date__gt=datetime.now()))
    serializer_class = QuizSerializer
