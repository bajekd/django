from django.http import JsonResponse
from django.http.response import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room
from .serializers import (RoomCreateSerializer, RoomSerializer,
                          RoomUpdateSerializer)


class IsUserInRoomView(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {"room_code": self.request.session.get("room_code")}

        return JsonResponse(data, status=status.HTTP_200_OK)


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailsView(APIView):
    def get(self, request, format=None, **kwargs):
        room_code = self.kwargs["room_code"]

        room = Room.objects.filter(room_code=room_code).first()
        if room:
            data = RoomSerializer(room).data
            data["is_host"] = self.request.session.session_key == room.host

            return Response(data, status=status.HTTP_200_OK)

        return Response({"Room Not Found": "Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)


class RoomCreateView(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = RoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.validated_data["guest_can_pause"]
            votes_to_skip = serializer.validated_data["votes_to_skip"]
            host = self.request.session.session_key

            room = Room.objects.filter(host=host).first()
            if room:
                return Response(
                    {"Conflict": "You already are host of the room!"},
                    status=status.HTTP_409_CONFLICT,
                )

            room = Room.objects.create(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
            self.request.session["room_code"] = room.room_code

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomUpdateView(APIView):
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = RoomUpdateSerializer(data=request.data)
        if serializer.is_valid():
            room_code = serializer.validated_data["room_code"]
            guest_can_pause = serializer.validated_data["guest_can_pause"]
            votes_to_skip = serializer.validated_data["votes_to_skip"]
            user_id = self.request.session.session_key

            room = Room.objects.filter(room_code=room_code, host=user_id).first()
            if room:
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=("guest_can_pause", "votes_to_skip"))

                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

            return Response({"Forbidden": "You are not the host of this room"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomJoinView(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        room_code = request.data.get("room_code")
        room = Room.objects.filter(room_code=room_code).first()
        if room:
            self.request.session["room_code"] = room_code

            return Response({"Success": "Room Joined!"}, status=status.HTTP_200_OK)

        return Response({"Bad Request": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST)


class RoomLeaveView(APIView):
    def post(self, request, format=None):
        host = self.request.session.session_key
        room_code = self.request.session.pop("room_code")
        Room.objects.filter(room_code=room_code, host=host).delete()

        return Response({"Success": "You left room. If you were host - room was deleted"}, status=status.HTTP_200_OK)
