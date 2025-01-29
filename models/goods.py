from db import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class ContainerModel(db.Model):
    __tablename__ = 'container'
    id = db.Column(db.String(80), primary_key=True)
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
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    container_id = db.Column(db.String(80), db.ForeignKey('container.id'))
    customs_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(80), nullable=True, default='detained')
    reason_for_detention = db.Column(db.String(200), nullable=True)
    perishable = db.Column(db.Boolean, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    storehouse_id = db.Column(db.Integer, db.ForeignKey('storehouse.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref='goods')
    container = db.relationship('ContainerModel', backref='goods')
    storehouse = db.relationship('Storehouse', backref='goods')
    user = db.relationship('UserModel', backref='goods')