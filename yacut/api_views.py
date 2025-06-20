from http import HTTPStatus

from flask import request, jsonify

from . import app
from .constants import (
    ERROR_NO_REQUEST_BODY,
    ERROR_NO_URL_FIELD,
    ERROR_ID_NOT_FOUND,
    DEFAULT_SHORT_ID_MAX_LENGTH,
    VALID_CUSTOM_ID_RE,
    ERROR_INVALID_CUSTOM_ID,
)
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_short():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(ERROR_NO_REQUEST_BODY)

    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_NO_URL_FIELD)

    custom_id = data.get('custom_id')

    if custom_id:
        if (len(custom_id) > DEFAULT_SHORT_ID_MAX_LENGTH or
                not VALID_CUSTOM_ID_RE.fullmatch(custom_id)):
            raise InvalidAPIUsage(ERROR_INVALID_CUSTOM_ID)

    try:
        url_map = URLMap.create(
            original=data['url'],
            custom_id=custom_id
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url_map = URLMap.get_by_short_id(short_id)
    if not url_map:
        raise LookupError(ERROR_ID_NOT_FOUND)

    result = {'url': url_map.to_dict()['url']}
    return jsonify(result), HTTPStatus.OK
