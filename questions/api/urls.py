from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("locationlist/<str:cmd>/",
        qv.locationList,
        name='sido-list'),

    path("locationlist/<str:cmd>/<str:sidocode>/",
        qv.locationList,
        name='sigungu-list'),
    
    path("locationlist/<str:cmd>/<str:sidocode>/<str:sigungucode>/",
    qv.locationList,
    name='eupmyundong-list'),

    path("questions/<int:id>/answers/", 
        qv.AnswerListAPIView.as_view(),
        name="answer-list"),

    path("questions/<int:id>/answer/", 
        qv.AnswerCreateAPIView.as_view(),
        name="create-answer"),

    path("answers/<int:id>/", 
        qv.AnswerRUDAPIView.as_view(),
        name="answer-detail"),

    path("answers/<int:pk>/like/",
        qv.AnswerLikeAPIView.as_view(),
        name="answer-like"),

    path("answers/<int:pk>/accept/",
        qv.AnswerAcceptAPIView.as_view(),
        name="answer-accept")        
]