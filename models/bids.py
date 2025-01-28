from db import db
from datetime import datetime

class BidModel(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('buyer.user_id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    good = db.relationship('GoodModel', back_populates='bids')
    auction = db.relationship('Auction', backref='bids')
    buyer = db.relationship('Buyer', backref='bids')