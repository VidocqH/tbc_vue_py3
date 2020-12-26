from app.api import bp
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    if status_code == 401:
        response = jsonify({'message': payload, 'code': 50014})
    else:
        response = jsonify({'message': payload, 'code': status_code})
    # response.status_code = 20000
    return response

def bad_request(message):
    """400 error request"""
    return error_response(400, message)

@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)