from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    answer = {'error':HTTP_STATUS_CODES.get(status_code, 'Error')}
    if message:
        answer['message'] = message
    response = jsonify(answer)
    response.status_code = status_code
    return response