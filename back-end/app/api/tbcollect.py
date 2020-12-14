from flask import jsonify, request
from app.api import bp
from app.api.data_getter.collectShop import getTaobaoShopSoup, getShopListFromTaobaoSoup
from app.api.data_getter.nohead_browser import isBrowserOpened
from app.database.models import Shops, TaobaoAccount
from app.database.database import session
from app.api.auths import token_auth

@bp.route('/tbcollect/<tbaccount>', methods=['POST'])
@token_auth.login_required
def tbcollect(tbaccount):
    # todo Keyword random
    data = request.get_json()
    keyword = str(data['keyword'])
    tbAcc = session.query(TaobaoAccount).filter(TaobaoAccount.username == tbaccount).first()
    if not tbAcc:
        return jsonify({'message': 'Taobao account doesn\'t found', 'code': 74147})
    tbpassword = tbAcc.decryptPWD(tbAcc.password_KEYencrypt)
    content = getTaobaoShopSoup(keyword, tbaccount, tbpassword)
    # if keyword not in str(driver.title):
        # return jsonify({'message': 'Login error', 'code': 74147})
    if type(content) == dict:
        return content # not the contents, it's now a error message
    res = getShopListFromTaobaoSoup(content)
    if type(res) == str:
        return jsonify({'message': res, 'code': 74147})
    return jsonify({'code': 20000})

@bp.route('/tbcollect/<tbaccount>', methods=['DELETE'])
@token_auth.login_required
def stopCollect(tbaccount):
    if isBrowserOpened(tbaccount):
        return jsonify({'message': tbaccount, 'code': 20000})
    return jsonify({'code': 70001})