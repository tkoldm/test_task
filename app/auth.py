from flask_login import current_user, login_user
from flask_httpauth import HTTPBasicAuth
from app import logger
from app.models.user_model import User
from app.queries import check_user_login
from app.errors import error_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = check_user_login(username, password)
    if user:
        login_user(user)
        logger.info(f'user:{current_user.username} - logged in')
        return True
    else:
        return False

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)