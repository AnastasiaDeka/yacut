from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    URL,
)

from flask_wtf import FlaskForm

from .constants import (
    MIN_SHORT_ID_LENGTH,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    VALID_CUSTOM_ID_RE,
    CUSTOM_ID_ERROR_MESSAGE,
)


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(),
            URL(),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(min=MIN_SHORT_ID_LENGTH,
                   max=DEFAULT_SHORT_ID_MAX_LENGTH),
            Regexp(
                VALID_CUSTOM_ID_RE,
                message=CUSTOM_ID_ERROR_MESSAGE,
            ),
        ],
    )
    submit = SubmitField('Создать')
