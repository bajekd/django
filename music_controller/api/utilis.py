import random
import string

from django.conf import settings


def generate_unique_room_code():
    from .models import Room

    length = getattr(settings, "ROOM_CODE_LENGTH", 24)
    while True:
        possible_chars = string.ascii_letters + string.digits
        room_code = "".join(random.choices(possible_chars, k=length))

        if not Room.objects.filter(room_code=room_code).exists():
            break

    return room_code
