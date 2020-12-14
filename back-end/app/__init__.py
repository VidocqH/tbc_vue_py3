from flask import Flask, _app_ctx_stack
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from config import Config
from sqlalchemy.orm import scoped_session
#from .database.database import engine,SessionLocal,Base

# Flask-SQLAlchemy Plugin
# db = SQLAlchemy()
# Flask-Migrate Plugin
# migrate = Migrate()

def create_app(config_class=Config):
    # models.Base.metadata.create_all(bind=engine)

    app = Flask(__name__)
    app.config.from_object(config_class)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    # Init Flask-SQLAlchemy
    # db.init_app(app)
    # Init Flask-Migrate
    # migrate.init_app(app, db)

    # Register blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

#from app import models
from app.database import models