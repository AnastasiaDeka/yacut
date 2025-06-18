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
    MAX_ORIGINAL_LINK_LENGTH,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    CUSTOM_ID_ALLOWED_RE,
    CUSTOM_ID_ERROR_MESSAGE,
)


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(),
            URL(),
            Length(max=MAX_ORIGINAL_LINK_LENGTH),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=DEFAULT_SHORT_ID_MAX_LENGTH),
            Regexp(
                CUSTOM_ID_ALLOWED_RE,
                message=CUSTOM_ID_ERROR_MESSAGE,
            ),
        ],
    )
    submit = SubmitField('Создать')
