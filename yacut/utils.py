import random

from .models import URLMap
from .constants import (
    DEFAULT_SHORT_ID_MIN_LENGTH,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    ALLOWED_CHARACTERS
)


def get_unique_short_id(length=DEFAULT_SHORT_ID_MIN_LENGTH):
    """Генерация уникального короткого идентификатора переменной длины."""
    if length > DEFAULT_SHORT_ID_MAX_LENGTH:
        raise ValueError(
            "Превышена максимально допустимая длина идентификатора."
        )

    while True:
        short_id = ''.join(
            random.choices(ALLOWED_CHARACTERS, k=length)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
