from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("room_code", "host", "guest_can_pause", "votes_to_skip", "created_at")


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("guest_can_pause", "votes_to_skip")


class RoomUpdateSerializer(serializers.ModelSerializer):
    room_code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ("room_code", "guest_can_pause", "votes_to_skip")
