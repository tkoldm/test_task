from flask_login import current_user, login_user
from flask_httpauth import HTTPBasicAuth
from app.models.user_model import User
from app.errors import error_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None or user.remove_date:
        return False
    if user.password == password:
        login_user(user)
        return True
    else:
        return False

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)