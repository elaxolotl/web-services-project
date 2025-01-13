from flask import Flask
from flask_smorest import Api
from db import db
from resources.goods import goods_bp
from resources.auctions import auctions_bp
from resources.users import users_bp
from resources.frontend import frontend_bp
from flask_security import Security, SQLAlchemySessionUserDatastore
from models.users import UserModel, Role
from models.goods import GoodModel
from flask_jwt_extended import JWTManager
import secrets
from flask_apscheduler import APScheduler
from datetime import datetime
from models.bids import BidModel

scheduler = APScheduler()
secret_key = secrets.token_hex(32)

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Cargo"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SECRET_KEY"] = secret_key
    app.config['SECURITY_REGISTERABLE'] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    
    jwt = JWTManager(app)
    
    db.init_app(app)
       
    api = Api(app)
    api.register_blueprint(goods_bp)
    api.register_blueprint(auctions_bp)
    api.register_blueprint(users_bp)
    api.register_blueprint(frontend_bp, exclude_from_spec=True)
    
    with app.app_context():
        db.create_all()
        db.session.commit()

        
    user_datastore = SQLAlchemySessionUserDatastore(db.session, UserModel, Role)
    security = Security(app, user_datastore)
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    
    @scheduler.task('interval', id='my_job', hours=24)
    def check_due_dates():
        goods = GoodModel.query.filter(GoodModel.due_date <= datetime.utcnow(), GoodModel.status == 'on_sale').all()

        for good in goods:
            bids = BidModel.query.filter_by(good_id=good.id)
            if bids:
                highest_bid = max(bids, key=lambda bid: bid.value)
                good.winner_id = highest_bid.user_id
                good.status = 'sold'
                db.session.commit()

    return app