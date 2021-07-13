from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import QuizViewSet, main_api_view, QuizQuestionViewSet, QuestionViewSet

router = SimpleRouter()
router.register("quiz", QuizViewSet)

quiz_questions_router = NestedSimpleRouter(router, r'quiz')
quiz_questions_router.register(r'questions', QuizQuestionViewSet)

question_router = SimpleRouter()
question_router.register("questions", QuestionViewSet)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    *router.urls,
    *quiz_questions_router.urls,
    *question_router.urls
]
