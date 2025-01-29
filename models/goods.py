from db import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Container(db.Model):
    __tablename__ = 'container'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class Storehouse(db.Model):
    __tablename__ = 'storehouse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(200), nullable=False)

class GoodModel(db.Model):
    __tablename__ = 'goods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'), nullable=False)
    customs_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    opening_price = db.Column(db.Float, nullable=False)
    guarantee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), nullable=False, default='detained')
    reason_for_detention = db.Column(db.String(200), nullable=True)
    perishable = db.Column(db.Boolean, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    storehouse_id = db.Column(db.Integer, db.ForeignKey('storehouse.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    category = db.relationship('Category', backref='goods')
    container = db.relationship('Container', backref='goods')
    storehouse = db.relationship('Storehouse', backref='goods')
    customs_officer = db.relationship('UserModel', backref='goods')

class Auction(db.Model):
    __tablename__ = 'auction'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    good = db.relationship('GoodModel', backref='auction')