from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import QuizViewSet, main_api_view

router = SimpleRouter()
router.register("quiz", QuizViewSet)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    *router.urls
]
