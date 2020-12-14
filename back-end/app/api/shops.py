from app.database.models import Shops
from app.database.database import session
from flask import jsonify
from app.api import bp
from app.api.auths import token_auth

@bp.route('/shops', methods=['GET'])
@token_auth.login_required
def tbshops():
    shops = session.query(Shops).all()
    return jsonify({'data': [shop.to_dict() for shop in shops], 'code':20000})