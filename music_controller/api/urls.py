from django.urls import path

from .views import (IsUserInRoomView, RoomCreateView, RoomDetailsView,
                    RoomJoinView, RoomLeaveView, RoomListView, RoomUpdateView)

app_name = "api"

urlpatterns = [
    path("", RoomListView.as_view(), name="room_list"),
    path("room/<str:room_code>", RoomDetailsView.as_view(), name="room_details"),
    path("create/", RoomCreateView.as_view(), name="room_create"),
    path("update/", RoomUpdateView.as_view(), name="room_update"),
    path("join/", RoomJoinView.as_view(), name="room_join"),
    path("leave_room/", RoomLeaveView.as_view(), name="room_leave"),
    path("is_user_in_room/", IsUserInRoomView.as_view(), name="is_user_in_room"),
]
