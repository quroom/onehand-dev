from django.urls import path
from users.api.views import UserAPIView, ProfileAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view(), name='current-user'),
    path('profile/', ProfileAPIView.as_view(), name='current-profile')
]