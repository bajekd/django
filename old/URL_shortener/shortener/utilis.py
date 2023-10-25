import random
from django.conf import settings
import string
import random

SHORT_CODE_LENGTH = getattr(settings, "SHORT_CODE_LENGTH", 3)


def create_shortcode(instance, size=SHORT_CODE_LENGTH):
    new_code = code_generator(size)
    ShortenerURL = instance.__class__  # way to avoid circling around import
    query_exists = ShortenerURL.objects.filter(short_code=new_code).exists()
    if query_exists:
        return create_shortcode(instance=instance, size=size)
    return new_code


def code_generator(size=SHORT_CODE_LENGTH, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
