from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from questions.api.permissions import IsAuthorOrReadOnly
from questions.api.serializers import AnswerSerializer, QuestionSerializer
from questions.models import Answer, Question

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)        

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        request_user = self.request.user
        id = self.kwargs.get("id")
        question = get_object_or_404(Question , id=id)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")
        serializer.save(author=request_user, question=question)

class AnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_id = self.kwargs.get('id')
        return Answer.objects.filter(question__id=kwarg_id).order_by('created_at')

class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Answer.objects.all().order_by('created_at')
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]