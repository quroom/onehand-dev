from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("questions/<int:pk>/answers/", 
    qv.AnswerListAPIView.as_view(),
    name="answer-list"),

    path("questions/<int:pk>/answer/", 
        qv.AnswerCreateAPIView.as_view(),
        name="create-answer"),

    path("answers/<int:pk>/", 
        qv.AnswerRUDAPIView.as_view(),
        name="answer-detail")    
        
]