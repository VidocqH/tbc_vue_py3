from app.database.models import TaobaoAccount
from app.database.database import session
from app.api import bp
from flask import jsonify, url_for, current_app, request
from app.api.auths import token_auth
import os
import shutil
from app.api.data_getter.collectShop import randomKeyWord

@bp.route('/tbaccounts/<int:id>', methods=['POST'])
@token_auth.login_required
def create_tbaccounts(id):
    data = request.get_json()
    data['owner_id'] = id
    if not data:
        return bad_request('Need to post data')
    message = ''
    if 'username' not in data or not data.get('username', None):
        message = 'Username invalid'
    if 'password' not in data or not data.get('password', None):
        message = 'Password invalid'
    if session.query(TaobaoAccount).filter(TaobaoAccount.username==data.get('username', None)).first():
        message = 'Username exists'
    if message != '':
        return bad_request(message)
    
    tbacc = TaobaoAccount()
    tbacc.from_dict(data)
    session.add(tbacc)
    session.commit()
    response = jsonify({'data':tbacc.to_dict(), 'code': 20000})
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=tbacc.owner_id)
    return response

@bp.route('/tbaccounts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_tbaccounts(id):
    accs = session.query(TaobaoAccount).filter(TaobaoAccount.owner_id == id).all()
    if accs == None:
        return error_response(404, 'User not found!')
    data = []
    for acc in accs:
        acc = acc.to_dict()
        acc['keyword'] = randomKeyWord()
        data.append(acc)
    return jsonify({'data': data, 'code': 20000})

@bp.route('/tbaccounts/<int:id>', methods=['PUT'])
@token_auth.login_required
def modify_tbaccount(id):
    data = request.get_json()
    acc = session.query(TaobaoAccount).filter(TaobaoAccount.username == data.get('username', None)).first()
    if acc.status:
        return bad_request('Account is running')
    if not data:
        return bad_request('You must post JSON data')
    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Username invalid'
    if 'password' in data and not data.get('password', None):
        message['password'] = 'Password invalid'
    if message:
        return bad_request(message)

    acc.from_dict(data)
    session.commit()
    return jsonify({'data': acc.to_dict(), 'code': 20000})

@bp.route('/tbaccounts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_tbaccount(id):
    data = request.get_json()
    acc = session.query(TaobaoAccount).filter(TaobaoAccount.username == data.get('username', None)).first()
    if not data:
        return bad_request('You must post JSON data')
    session.delete(acc)
    session.commit()
    user_data = os.getcwd() + "/app/api/data_getter/userdata/" + str(acc.username)
    try:
        shutil.rmtree(user_data)
    except:
        pass
    return jsonify({'code': 20000})
