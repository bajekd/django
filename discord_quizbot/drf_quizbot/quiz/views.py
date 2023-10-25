import pdb

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question
from .serializers import RandomQuestionSerializer


class RandomQuestion(APIView):
    def get(self, request, formate=None, **kwargs):
        question = Question.objects.filter(is_active=True).order_by("?").first()
        serializer = RandomQuestionSerializer(question)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        