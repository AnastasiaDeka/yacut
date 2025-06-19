from http import HTTPStatus

from flask import request, jsonify

from . import app
from .models import URLMap
from .constants import (
    ERROR_NO_REQUEST_BODY,
    ERROR_NO_URL_FIELD,
    ERROR_ID_NOT_FOUND
)


@app.route('/api/id/', methods=['POST'])
def create_short():
    data = request.get_json(silent=True)

    if data is None:
        raise ValueError(ERROR_NO_REQUEST_BODY)

    if 'url' not in data:
        raise ValueError(ERROR_NO_URL_FIELD)

    custom_id = data.get('custom_id')

    url_map = URLMap.create(
        original=data['url'],
        custom_id=custom_id
    )

    return jsonify(url_map.to_dict(request.host_url)), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url_map = URLMap.get_by_short_id(short_id)
    if not url_map:
        raise LookupError(ERROR_ID_NOT_FOUND)
    return jsonify(url_map.to_api_dict()), HTTPStatus.OK
