from django.urls import include, path

from .views import (AuthURLView, CurrentSongView, IsAuthenticatedView, PauseSongView, PlaySongView, spotify_callback,
                    SkipSongView)

app_name = "spotify"

urlpatterns = [
    path("get-auth-url/", AuthURLView.as_view(), name="auth_get_url"),
    path("redirect/", spotify_callback, name="auth_callback"),
    path("is-authenticated/", IsAuthenticatedView.as_view(), name="auth_check"),
    path("current-song/", CurrentSongView.as_view(), name="current_song"),
    path("play/", PlaySongView.as_view(), name="play_song"),
    path("pause/", PauseSongView.as_view(), name="pause_song"),
    path("skip/", SkipSongView.as_view(), name="skip_song")
]
