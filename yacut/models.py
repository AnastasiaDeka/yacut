import random
from datetime import datetime

from . import db
from .constants import (
    VALID_CUSTOM_ID_RE,
    ERROR_INVALID_CUSTOM_ID,
    ERROR_CUSTOM_ID_EXISTS,
    DEFAULT_SHORT_ID_MIN_LENGTH,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    ALLOWED_CHARACTERS,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(DEFAULT_SHORT_ID_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(DEFAULT_SHORT_ID_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    @staticmethod
    def get_by_short_id(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
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

    @staticmethod
    def create(original, custom_id=None):
        if custom_id:
            if not VALID_CUSTOM_ID_RE.fullmatch(custom_id):
                raise ValueError(ERROR_INVALID_CUSTOM_ID)
            if URLMap.query.filter_by(short=custom_id).first():
                raise ValueError(ERROR_CUSTOM_ID_EXISTS)
            short = custom_id
        else:
            short = URLMap.get_unique_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self, host_url):
        return {
            'url': self.original,
            'short_link': host_url + self.short
        }

    def to_api_dict(self):
        return {'url': self.original}
