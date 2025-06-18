import string
import re


DEFAULT_SHORT_ID_MIN_LENGTH = 6
DEFAULT_SHORT_ID_MAX_LENGTH = 16
MAX_ORIGINAL_LINK_LENGTH = 2048

ALLOWED_CHARACTERS = string.ascii_letters + string.digits

VALID_CUSTOM_ID_RE = re.compile(r'^[A-Za-z0-9_]{1,16}$')
CUSTOM_ID_ALLOWED_RE = r'^[a-zA-Z0-9]+$'

CUSTOM_ID_ERROR_MESSAGE = 'Допустимы только символы a-z, A-Z, 0-9'
ERROR_NO_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_NO_URL_FIELD = '"url" является обязательным полем!'
ERROR_INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
ERROR_CUSTOM_ID_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
ERROR_ID_NOT_FOUND = 'Указанный id не найден'
