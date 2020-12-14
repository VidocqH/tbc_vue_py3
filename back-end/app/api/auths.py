from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.database.database import session
from app.database.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter(User.username==username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

@token_auth.verify_token
def verify_token(token):
    g.current_user = User.verify_jwt(token) if token else None
    if g.current_user:
        g.current_user.ping()
        session.commit()
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)