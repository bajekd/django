from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Score
from .serializers import ScoreSerializer


class UpdateScore(APIView):
    def post(self, request, format=None):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            points = serializer.validated_data["points"]

            if Score.objects.filter(name=name).exists():
                serializer = Score.objects.get(name=name)
                serializer.points = F("points") + points

            serializer.save()

            return Response(None, status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Leaderboard(APIView):
    def get(self, request, formate=None, **kwargs):
        scores = Score.objects.all().order_by("-points")[:15]
        serializer = ScoreSerializer(scores, many=True)

        return Response(serializer.data)
