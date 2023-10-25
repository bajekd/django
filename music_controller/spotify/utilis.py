import pdb
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from .models import SpotifyToken, Vote
import pdb

BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_token(session_id):
    try:
        user_token = SpotifyToken.objects.get(user=session_id)
    except SpotifyToken.DoesNotExist:
        user_token = None

    return user_token


def create_or_update_user_token(session_id, token_type, access_token, refresh_token, expires_in):
    token = get_user_token(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if token:
        # Update
        token.token_type = token_type
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in

        token.save(update_fields=("token_type", "access_token", "refresh_token", "expires_in"))
    else:
        # Create
        token = SpotifyToken.objects.create(
            user=session_id,
            token_type=token_type,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )


def is_spotify_authenticated(session_id):
    token = get_user_token(session_id)

    if not token:
        return False

    expiration_date = token.expires_in
    if expiration_date <= timezone.now():
        refresh_spotify_token(session_id, token)

    return True


def refresh_spotify_token(session_id, token_to_refresh):
    refresh_token = token_to_refresh.refresh_token
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": getattr(settings, "SPOTIFY_CLIENT_ID"),
            "client_secret": getattr(settings, "SPOTIFY_CLLIENT_SECRET"),
        },
    ).json()

    token_type = response.get("token_type")
    access_token = response.get("access_token")
    expires_in = response.get("expires_in")

    create_or_update_user_token(session_id, token_type, access_token, refresh_token, expires_in)


def update_room_song(room, song_id):
    if room.current_song != song_id:
        room.current_song = song_id
        room.save(update_fields=("current_song",))
        Vote.objects.filter(room=room).delete()


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    token = get_user_token(session_id)
    if not token:
        return {"status": 400, "message": "Spotify token does not exist!"}

    header = {"Content-Type": "application/json", "Authorization": f"Bearer {token.access_token}"}

    if post_:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=header)
    elif put_:
        response = requests.put(f"{BASE_URL}{endpoint}", headers=header)
    else:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=header)

    try:
        return response.json()
    except:
        return {"Error": "Issue with request"}


def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)


def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)


def skip_song(session_id):
    return execute_spotify_api_request(session_id, "player/next", post_=True)
