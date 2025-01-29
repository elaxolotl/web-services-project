from flask import Flask, render_template
from flask_smorest import Api
from db import db
from resources.goods import goods_bp
from resources.bids import bids_bp
from resources.users import users_bp
from resources.auctions import auctions_bp
from resources.storehouses import storehouses_bp
from resources.containers import containers_bp
from flask_security import Security, SQLAlchemySessionUserDatastore
from models.users import UserModel, Role
from models.goods import Category
from models.auctions import AuctionModel
from flask_jwt_extended import JWTManager
import secrets
from flask_apscheduler import APScheduler
from datetime import datetime
from models.bids import BidModel
from config import Config
from notifications import send_notification
import asyncio

secret_key = secrets.token_hex(32)

def create_app(db_url=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    jwt = JWTManager(app)
    jwt.init_app(app)
    db.init_app(app)       
    api = Api(app)
    api.register_blueprint(goods_bp)
    api.register_blueprint(bids_bp)
    api.register_blueprint(users_bp)
    api.register_blueprint(auctions_bp)
    api.register_blueprint(storehouses_bp)
    api.register_blueprint(containers_bp)
    
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
        auctions = AuctionModel.query.filter(AuctionModel.due_date <= datetime.utcnow()).all()

        for auction in auctions:
            bids = BidModel.query.filter_by(auction_id=auction.id)
            if bids:
                highest_bid = max(bids, key=lambda bid: bid.value)
                winner = UserModel.query.get(highest_bid.user_id)
                asyncio.run(send_notification(winner.email, winner.email, winner.number, "Your bid has won the auction!", auction.id))
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
        db.drop_all()
        db.create_all()
        populate_initial_data()
        db.session.commit()

def populate_initial_data():
    roles = ['Customs officer', 'Buyer', 'Owner']
    categories = ['Furniture', 'Cars', 'Clothes']

    for role in roles:
        new_role = Role(name=role)
        db.session.add(new_role)

    for category in categories:
        new_category = Category(name=category)
        db.session.add(new_category)

    db.session.commit()