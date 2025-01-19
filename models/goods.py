from db import db
from datetime import datetime

class GoodModel(db.Model):
    __tablename__ = 'goods'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Product Information
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    manufacturer_details = db.Column(db.String(200), nullable=True)
    
    # Financial Information
    opening_price = db.Column(db.Float, nullable=False)
    guarantee = db.Column(db.Float, nullable=False)
    
    # Status and Reason
    status = db.Column(db.String(80), nullable=False, default='detained')
    reason_for_detention = db.Column(db.String(200), nullable=True)
    
    # Perishable Information
    perishable = db.Column(db.Boolean, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    
    # Storage Details
    store = db.Column(db.String(80), nullable=True)
    container_id = db.Column(db.String(80), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Traking
    customs_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    bids = db.relationship('BidModel', back_populates='good')