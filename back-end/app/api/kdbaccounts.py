from app.database.models import KDBAccount, User
from app.database.database import session
from app.api import bp
from flask import jsonify, url_for, current_app, request
from app.api.auths import token_auth
import os
import shutil

@bp.route('/kdbaccounts/<int:id>', methods=['POST'])
@token_auth.login_required
def create_kdbaccounts(id):
    data = request.get_json()
    if not data:
        return bad_request('Need to post data')
    message = ''
    if 'username' not in data or not data.get('username', None):
        message = 'Username invalid'
    if 'password' not in data or not data.get('password', None):
        message = 'Password invalid'
    if message != '':
        return bad_request(message)

    for acc in session.query(KDBAccount).filter(KDBAccount.owner_id == id).all():
        print(acc.to_dict())
        if acc.to_dict()['username'] == str(data['username']):
            return jsonify({'message': 'Account exists!', 'code': 70000})
    kdbacc = KDBAccount()
    data['owner_id'] = id
    kdbacc.from_dict(data)
    # kdbacc.user_id += [user]
    session.add(kdbacc)
    session.commit()
    response = jsonify({'data': kdbacc.to_dict(), 'code': 20000})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=id)
    return response

@bp.route('/kdbaccounts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_kdbaccounts(id):
    accs = session.query(KDBAccount).filter(KDBAccount.owner_id == id).all()
    # if g.current_user == user:
    #     return jsonify(User.query.get_or_404(id).to_dict())
    if accs == None:
        return error_response(404, 'User not found!')
    return jsonify({'data': [acc.to_dict() for acc in accs], 'code': 20000})

@bp.route('/kdbaccounts/<int:id>', methods=['PUT'])
@token_auth.login_required
def modify_kdbaccount(id):
    data = request.get_json()
    acc = session.query(KDBAccount).filter(KDBAccount.owner_id == id, KDBAccount.username == data.get('username', None)).first()
    if not data:
        return bad_request('You must post JSON data')
    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Username invalid'
    if 'password' in data and not data.get('password', None):
        message['password'] = 'Password invalid'
    if message:
        return bad_request(message)

    data['owner_id'] = id
    acc.from_dict(data)
    session.commit()
    return jsonify({'data': acc.to_dict(), 'code': 20000})

@bp.route('/kdbaccounts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_kdbaccount(id):
    data = request.get_json()
    acc = session.query(KDBAccount).filter(KDBAccount.owner_id == id, KDBAccount.username == data.get('username', None)).first()
    if not data:
        return bad_request('You must post JSON data')
    session.delete(acc)
    session.commit()
    return jsonify({'code': 20000})
