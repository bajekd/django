from django.conf import settings
from django.shortcuts import redirect
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from api.models import Room
from .models import Vote
from .utilis import (
    create_or_update_user_token,
    is_spotify_authenticated,
    update_room_song,
    execute_spotify_api_request,
    pause_song,
    play_song,
    skip_song,
)


class AuthURLView(APIView):
    def get(self, request, format=None):
        permission_scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        url = (
            requests.Request(
                "GET",
                "https://accounts.spotify.com/authorize",
                params={
                    "scope": permission_scope,
                    "response_type": "code",
                    "redirect_uri": getattr(settings, "SPORIFY_REDIRECT_URI"),
                    "client_id": getattr(settings, "SPOTIFY_CLIENT_ID"),
                },
            )
            .prepare()
            .url
        )

        return Response({"url": url}, status=status.HTTP_200_OK)


def spotify_callback(request):
    auth_code = request.GET.get("code")
    # error = request.GET.get("error")

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": getattr(settings, "SPORIFY_REDIRECT_URI"),
            "client_id": getattr(settings, "SPOTIFY_CLIENT_ID"),
            "client_secret": getattr(settings, "SPOTIFY_CLLIENT_SECRET"),
        },
    ).json()

    token_type = response.get("token_type")
    access_token = response.get("access_token")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")

    create_or_update_user_token(request.session.session_key, token_type, access_token, refresh_token, expires_in)

    return redirect("frontend:home")


class IsAuthenticatedView(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)

        return Response({"is_authenticated": is_authenticated}, status=status.HTTP_200_OK)


class CurrentSongView(APIView):
    def get(self, request, format=None):
        try:
            room_code = self.request.session.get("room_code")
            room = Room.objects.get(room_code=room_code)
            host = room.host
        except:
            return Response(
                {"status": 404, "message": "Room not found or invalid room code"}, status=status.HTTP_404_NOT_FOUND
            )

        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)
        if "Error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if "item" not in response:
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        item = response.get("item")
        duration = item.get("duration_ms")
        progress = response.get("progress_ms")
        album_cover = item.get("album").get("images")[0].get("url")
        is_playing = response.get("is_playing")
        song_id = item.get("id")

        artists = ""
        for i, artist in enumerate(item.get("artists")):
            if i > 0:
                artists += ", "
            name = artist.get("name")
            artists += name

        votes = len(Vote.objects.filter(room=room, song_id=song_id))
        song = {
            "title": item.get("name"),
            "artists": artists,
            "duration": duration,
            "time": progress,
            "image_url": album_cover,
            "is_playing": is_playing,
            "votes": votes,
            "votes_required": room.votes_to_skip,
            "id": song_id,
        }
        update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)


class PauseSongView(APIView):
    def put(self, request, format=None):
        try:
            room_code = self.request.session.get("room_code")
            room = Room.objects.get(room_code=room_code)
        except:
            return Response(
                {"status": 404, "message": "Given room_code or room does not exist!"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.request.session.session_key == room.host or room.guest_can_pause:
            response = pause_song(room.host)
            return Response(response, status=status.HTTP_200_OK)

        return Response(
            {"status": 403, "message": "You are not allowed to do this!"}, status=status.HTTP_403_FORBIDDEN
        )


class PlaySongView(APIView):
    def put(self, request, format=None):
        try:
            room_code = self.request.session.get("room_code")
            room = Room.objects.get(room_code=room_code)
        except:
            return Response(
                {"status": 404, "message": "Given room_code or room does not exist!"}, status=status.HTTP_404_NOT_FOUND
            )

        if self.request.session.session_key == room.host or room.guest_can_pause:
            response = play_song(room.host)
            return Response(response, status=status.HTTP_200_OK)

        return Response(
            {"status": 403, "message": "You are not allowed to do this!"}, status=status.HTTP_403_FORBIDDEN
        )


class SkipSongView(APIView):
    def post(self, request, format=None):
        try:
            room_code = self.request.session.get("room_code")
            room = Room.objects.prefetch_related("votes").get(room_code=room_code)
        except:
            return Response(
                {"status": 404, "message": "Given room_code or room does not exist!"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            Vote.objects.create(user=self.request.session.session_key, room=room, song_id=room.current_song)
        except IntegrityError:
            return Response(
                {"status": 409, "message": "For given song you can vote only once to skip it!"},
                status=status.HTTP_409_CONFLICT,
            )
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed_to_skip = room.votes_to_skip

        if (self.request.session.session_key == room.host) or (len(votes) >= votes_needed_to_skip):
            skip_song(room.host)
            votes.delete()
            return Response({"status": 200, "message": "Song skipped"}, status=status.HTTP_200_OK)

        return Response({"status": 200, "message": "+1 vote to skip song recived"}, status=status.HTTP_200_OK)
