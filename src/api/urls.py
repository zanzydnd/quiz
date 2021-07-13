from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from api.views import QuizViewSet, main_api_view, QuizQuestionViewSet, QuestionViewSet, ListQuizForUserView, \
    RetrieveAnswerForQuiz, QuizAnalysis, authenticate_user

router = SimpleRouter()
router.register("quiz", QuizViewSet)

quiz_questions_router = NestedSimpleRouter(router, r'quiz')
quiz_questions_router.register(r'questions', QuizQuestionViewSet)

question_router = SimpleRouter()
question_router.register("questions", QuestionViewSet)

user_quizes_router = SimpleRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version="v1",
        description="Quiz",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    path("quizes_for_user/", ListQuizForUserView.as_view(), name="quizes_for_user"),
    path("quiz/<int:quiz_id>/answer/", RetrieveAnswerForQuiz.as_view(), name="answer"),
    path("quiz/<int:pk>/analysis/<int:user_id>/", QuizAnalysis.as_view(), name="analysis"),
    path("auth", authenticate_user, name="auth"),
    *router.urls,
    *quiz_questions_router.urls,
    *question_router.urls,
    re_path("swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

]
