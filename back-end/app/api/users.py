from app.api import bp
from flask import jsonify, current_app, url_for, request
from app.api.errors import bad_request, error_response
from ..database.database import Base, SessionLocal, session
from ..database.models import User
import jwt
import base64
from app.api.auths import token_auth

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return bad_request('Need to post data')
    message = ''
    if 'username' not in data or not data.get('username', None):
        message = 'Username invalid'
    if 'password' not in data or not data.get('password', None):
        message = 'Password invalid'
    if session.query(User).filter(User.username==data.get('username', None)).first():
        message = 'Username exists'
    if message != '':
        return bad_request(message)
    
    user = User()
    user.from_dict(data)
    session.add(user)
    session.commit()
    response = jsonify({'data':user.to_dict(), 'code': 20000})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    user = session.query(User).filter(User.id == id).first()
    if user == None:
        return error_response(404, 'User not found!')
    return jsonify({'data': user.to_dict(), 'code': 20000})

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def modify_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data')
    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Username invalid'
    if 'password' in data and not data.get('password', None):
        message['password'] = 'Password invalid'
    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Username exists'
    if message:
        return bad_request(message)

    user.json_to_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.dict_to_json())

@bp.route('/users/<int:id>', methods=['DELETE'])
# @token_auth.login_required
def delete_user():
    pass

@bp.route('/users/logout', methods=['POST'])
def logout():
    return jsonify({'code': 20000})