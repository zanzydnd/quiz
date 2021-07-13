from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import QuizViewSet, main_api_view, QuizQuestionViewSet, QuestionViewSet, ListQuizForUserView, \
    RetrieveAnswerForQuiz, QuizAnalysis

router = SimpleRouter()
router.register("quiz", QuizViewSet)

quiz_questions_router = NestedSimpleRouter(router, r'quiz')
quiz_questions_router.register(r'questions', QuizQuestionViewSet)

question_router = SimpleRouter()
question_router.register("questions", QuestionViewSet)

user_quizes_router = SimpleRouter()
urlpatterns = [
    path("", main_api_view, name="empty_api"),
    path("quizes_for_user/", ListQuizForUserView.as_view(), name="quizes_for_user"),
    path("quiz/<int:quiz_id>/answer/", RetrieveAnswerForQuiz.as_view(), name="answer"),
    path("quiz/<int:pk>/analysis/<int:user_id>/", QuizAnalysis.as_view(), name="analysis"),
    *router.urls,
    *quiz_questions_router.urls,
    *question_router.urls
]
