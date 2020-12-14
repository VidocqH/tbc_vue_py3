from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base, session, engine
from datetime import datetime, timedelta
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import jwt
from flask import current_app, url_for
from hashlib import md5
import json
import base64

class Shops(Base, SerializerMixin):
    __tablename__ = 'Shops'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    shopName = Column(String(64))
    shopURL = Column(String(128))
    sellerName = Column(String(64))
    sellerURL = Column(String(128))
    sellerUid = Column(String(64), index=True, unique=True)
    sellerWangWangOnlineStatus = Column(String(16))
    sellerWangWangURL = Column(String(128))
    goodCommentRatio = Column(String(16))
    isConsumerInsure = Column(Boolean())
    isGoldSeller = Column(Boolean())
    numberOfFans = Column(Integer, default=-1)
    shopZone = Column(String(16), default='')
    numberOfItems = Column(Integer, default=-1)
    openingDate = Column(DateTime(), default=datetime(1970, 1, 1, 0, 0, 0))
    dsr_value = Column(Integer, default=-1)
    shopCategory = Column(String(64), default='')

# User_KDBAccount = Table(
#     """ The middle table between user and kdbaccount"""
#     'User_KDBAccount',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('User.id'), nullable=False, primary_key=True),
#     Column('kdb_id', Integer, ForeignKey('KDBAccount.id'), nullable=False, primary_key=True),
#     useexisting=True    
# )

class User(Base):
    __tablename__ = 'User'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128))
    last_seen = Column(DateTime(), default=datetime.utcnow())
    name = Column(String(64))
    # kdb_id = relationship("KDBAccount", secondary=User_KDBAccount, back_populates='user_id')

    def from_dict(self, dictData):
        """ Create a new uesr """
        self.username = dictData['username']
        self.password_hash = generate_password_hash(dictData['password'])

    def check_password(self, password):
        """ Check PWD, return type: Boolean """
        return check_password_hash(pwhash=self.password_hash, password=password)
    
    def to_dict(self):
        """ Transform class data into Dict """
        data = {
            'user_id': self.id,
            'username': self.username,
            'name': self.name,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        return data

    def ping(self):
        self.last_seen = datetime.utcnow()
        session.add(self)
    
    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    def get_jwt(self, expires_in=600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'name': self.name if self.name else self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return session.query(User).filter(User.id == payload.get('user_id')).first()
        # return User.query.get(payload.get('user_id'))


class KDBAccount(Base):
    __tablename__ = 'KDBAccount'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=False)
    password_hash = Column(String(128))
    owner_id = Column(Integer)
    # user_id = relationship("User", secondary=User_KDBAccount, back_populates='kdb_id')

    def encryptPWD(self, password):
        """ Encrypt password for store """
        encryptFunction = Fernet(private_key)
        encoded_pwd = str(password).encode()
        return encryptFunction.encrypt(encoded_pwd)

    def decryptPWD(self, encryptedPWD):
        """ Decrypt password for login """
        decryptFunction = Fernet(private_key)
        decrypted_pwd = decryptFunction.decrypt(encryptedPWD)
        return decrypted_pwd.decode()

    def from_dict(self, data):
        """ Create or modify an account"""
        self.username = data['username']
        self.password_hash = self.encryptPWD(data['password'])
        self.owner_id = data['owner_id']
        

    def to_dict(self):
        res_dict = {
            'username': self.username,
            # 'password': str(self.decryptPWD(self.password_KEYencrypt))
        }
        return res_dict

# KDBAccount.__table__.create(engine)

private_key = b'lyuEBUNrtcIP-ZkGNp_UYHhYHucaj2JOTH9Ryf0lQzs='
class TaobaoAccount(Base):
    __tablename__ = 'TaoBaoAccount'
    __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, index=True)
    username = Column(String(64), unique=True)
    password_KEYencrypt = Column(String(64))
    """ status: 0=NotRuning 1=Running 2=Waiting """
    status = Column(Integer, default=0)

    def encryptPWD(self, password):
        """ Encrypt password for store """
        encryptFunction = Fernet(private_key)
        encoded_pwd = str(password).encode()
        return encryptFunction.encrypt(encoded_pwd)

    def decryptPWD(self, encryptedPWD):
        """ Decrypt password for login """
        decryptFunction = Fernet(private_key)
        decrypted_pwd = decryptFunction.decrypt(encryptedPWD)
        return decrypted_pwd.decode()

    def from_dict(self, data):
        """ Create or modify an account"""
        try:
            self.owner_id = data['owner_id']
        except KeyError:
            pass
        self.username = data['username']
        self.password_KEYencrypt = self.encryptPWD(data['password'])

    def to_dict(self):
        res_dict = {
            'username': self.username,
            # 'password': str(self.decryptPWD(self.password_KEYencrypt))
            'status': self.status
        }
        return res_dict
