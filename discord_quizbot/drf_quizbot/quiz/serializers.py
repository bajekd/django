from rest_framework import serializers

from .models import Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "answer",
            "is_correct",
        )


class RandomQuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # related_name in model Question

    class Meta:
        model = Question
        fields = (
            "title",
            "points",
            "answers",
        )
