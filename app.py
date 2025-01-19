from flask import Flask, render_template
from flask_smorest import Api
from db import db
from resources.goods import goods_bp
from resources.auctions import auctions_bp
from resources.users import users_bp
from flask_security import Security, SQLAlchemySessionUserDatastore
from models.users import UserModel, Role, roles_users
from models.goods import GoodModel
from flask_jwt_extended import JWTManager
import secrets
from flask_apscheduler import APScheduler
from datetime import datetime
from models.bids import BidModel
from config import Config

secret_key = secrets.token_hex(32)

def create_app(db_url=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    jwt = JWTManager(app)
    jwt.init_app(app)
    db.init_app(app)       
    api = Api(app)
    api.register_blueprint(goods_bp)
    api.register_blueprint(auctions_bp)
    api.register_blueprint(users_bp)
    
    setup_security_schemes(api)
    
    create_database(app)
    
    
    user_datastore = SQLAlchemySessionUserDatastore(db.session, UserModel, Role)
    security = Security(app, user_datastore)
    
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    #scheduler task    
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

    @app.route('/')
    def landing_page():
        return render_template('index.html')

    @app.route('/features')
    def features_page():
        return render_template('features.html')

    return app

def setup_security_schemes(api):
    api_key_scheme = {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "API Key",
    }
    api.spec.components.security_scheme("Bearer", api_key_scheme)
    api.spec.options["security"] = [{"Bearer": []}]
    
def create_database(app):
    with app.app_context():
        db.create_all()
        db.session.commit()