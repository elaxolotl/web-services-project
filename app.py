from flask import Flask
from flask_smorest import Api
from db import db
from resources.goods import goods_bp
from resources.auctions import auctions_bp
from resources.users import users_bp
import os
from flask_login import LoginManager, login_manager, login_user
from flask_security import Security, SQLAlchemySessionUserDatastore
from models.users import UserModel, Role

def create_app(db_url=None):
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config["API_TITLE"] = "TraceUp"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config['SECURITY_REGISTERABLE'] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    
    db.init_app(app)
    
    api = Api(app)
    app.register_blueprint(goods_bp)
    app.register_blueprint(auctions_bp)
    app.register_blueprint(users_bp)
    
    with app.app_context():
        db.create_all()
        
    user_datastore = SQLAlchemySessionUserDatastore(db.session, UserModel, Role)
    security = Security(app, user_datastore)
    
    return app