from flask import jsonify
from app.api import bp
from app.api.data_getter.collectShop import getKandianbaoShopInfoSoup, getShopInfoFromKDBSoup
from app.database.models import Shops, KDBAccount
from app.database.database import session
from app.api.data_getter.nohead_browser import setBrowser, isBrowserOpened

@bp.route('/kdbcollect/<kdbaccount>', methods=['POST'])
def kdbcollect(kdbaccount):
    kdbAcc = session.query(KDBAccount).filter(KDBAccount.username == kdbaccount).first()
    if not kdbAcc:
        return jsonify({'message': 'KanDianBao account doesn\'t found', 'code': 74147})
    kdbpassword = kdbAcc.decryptPWD(kdbAcc.password_hash)
    shopList = session.query(Shops).filter(Shops.numberOfItems == -1)
    driver = setBrowser(kdbaccount, isMitmProxy=False)
    for shop in shopList:
        shopInfoAndDriver = getKandianbaoShopInfoSoup(shop.sellerName, kdbaccount, kdbpassword, driver)
        if type(shopInfoAndDriver) == str:
            if shopInfoAndDriver == '限额已耗尽':
                return jsonify({'message': kdbaccount + ': 限额已耗尽', 'code': 20000})
            return jsonify({'message': kdbaccount + ': ' + shopInfoAndDriver, 'code': 70001})
        getShopInfoFromKDBSoup(shop.sellerName, shopInfoAndDriver[0])
    return jsonify({'code': 20000})

@bp.route('/kdbcollect/<kdbaccount>', methods=['DELETE'])
def stopKdbCollect(kdbaccount):
    if isBrowserOpened(kdbaccount):
        return jsonify({'message': kdbaccount, 'code': 20000})
    return jsonify({'code': 70001})