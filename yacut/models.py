import random
from datetime import datetime

from flask import url_for
from . import db
from .constants import (
    ERROR_CUSTOM_ID_EXISTS,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    DEFAULT_SHORT_ID_MIN_LENGTH,
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
    def get_unique_short_id():
        while True:
            short_id = ''.join(
                random.choices(
                    ALLOWED_CHARACTERS, k=DEFAULT_SHORT_ID_MIN_LENGTH
                )
            )
            if not URLMap.get_by_short_id(short_id):
                return short_id

    @staticmethod
    def create(original, custom_id=None):
        if custom_id:
            if URLMap.get_by_short_id(custom_id):
                raise ValueError(ERROR_CUSTOM_ID_EXISTS)
            short = custom_id
        else:
            short = URLMap.get_unique_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(
                'follow_link',
                short=self.short, _external=True
            ),
        }
