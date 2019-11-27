from django.urls import path
from users.api.views import UserAPIView, ProfileDetailAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view(), name='current-user'),
    path('profile/', ProfileDetailAPIView.as_view(), name='current-profile')
]