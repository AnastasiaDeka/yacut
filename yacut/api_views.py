from http import HTTPStatus

from flask import request, jsonify

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id
from .constants import (
    VALID_CUSTOM_ID_RE,
    ERROR_NO_REQUEST_BODY,
    ERROR_NO_URL_FIELD,
    ERROR_INVALID_CUSTOM_ID,
    ERROR_CUSTOM_ID_EXISTS,
    ERROR_ID_NOT_FOUND
)


@app.route('/api/id/', methods=['POST'])
def create_short():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify(
            {'message': ERROR_NO_REQUEST_BODY}
        ), HTTPStatus.BAD_REQUEST

    if 'url' not in data:
        return jsonify(
            {'message': ERROR_NO_URL_FIELD}
        ), HTTPStatus.BAD_REQUEST

    custom_id = data.get('custom_id')

    if custom_id:
        if not VALID_CUSTOM_ID_RE.fullmatch(custom_id):
            return jsonify(
                {'message': ERROR_INVALID_CUSTOM_ID}
            ), HTTPStatus.BAD_REQUEST

        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify(
                {'message': ERROR_CUSTOM_ID_EXISTS}
            ), HTTPStatus.BAD_REQUEST

    short = custom_id if custom_id else get_unique_short_id()

    url_map = URLMap(original=data['url'], short=short)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': request.host_url + url_map.short
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if not url_map:
        return jsonify(
            {'message': ERROR_ID_NOT_FOUND}
        ), HTTPStatus.NOT_FOUND

    return jsonify({'url': url_map.original}), HTTPStatus.OK
