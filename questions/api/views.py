from django.http import JsonResponse, HttpResponse
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from questions.api.permissions import IsAuthorOrReadOnly, IsQuestionAuthorOrReadOnly, IsAuthenticatedOrQuestionListOnly
from questions.api.serializers import AnswerSerializer, QuestionSerializer
from questions.models import Answer, Question

import requests

def locationList(request, cmd, sidocode='None', sigungucode=''):
    base_url = "http://openapi.epost.go.kr/postal/retrieveLotNumberAdressAreaCdService/retrieveLotNumberAdressAreaCdService/"
    service_key = "zBR3IIhs2wZyfk5Z%2B89R%2BylLx6Tctaa7bKH9wyL9CXJUOguzrHlOFB0G2%2BQYEqpgrdy0RCYEro7jjqrthW5LoQ%3D%3D"
    if cmd == "sido":
        url = base_url + 'getBorodCityList' + "?ServiceKey=" + service_key
    elif cmd == "sigungu":
        url = base_url + 'getSiGunGuList' + "?ServiceKey=" + service_key + "&brtcCd=" + sidocode
    elif cmd == "eupmyundong":
        url = base_url + 'getEupMyunDongList' + "?ServiceKey=" + service_key + "&brtcCd=" + sidocode + "&signguCd=" + sigungucode
        

    response = requests.get(url)
    if response.status_code != 200:
        return HttpResponse(response.reason, status=response.status_code)
    else:
        return HttpResponse(response.text, status=status.HTTP_200_OK)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrQuestionListOnly, IsAuthorOrReadOnly]
    
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

class AnswerLikeAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = self.request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = self.request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AnswerAcceptAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_class = [IsQuestionAuthorOrReadOnly]

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        answer.is_accepted = False
        answer.save()
        question = answer.question
        question.is_question_done = False
        question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        if answer.question.is_question_done==True:
            raise ValidationError("이미 답변을 채택 했습니다.")
        answer.is_accepted = True
        answer.save()
        answer.question.is_question_done = True
        answer.question.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)