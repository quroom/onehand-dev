from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.permissions import IsAuthorOrReadOnly
from users.models import Profile
from users.api.serializers import UserDisplaySerializer,ProfileDisplaySerializer
from rest_framework.permissions import IsAuthenticated

class UserAPIView(APIView):

    def get(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)

class ProfileAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDisplaySerializer

class ProfileRUDAPIVuew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDisplaySerializer