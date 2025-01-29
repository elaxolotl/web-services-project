from db import db
from datetime import datetime

class BidModel(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    auction = db.relationship('AuctionModel', backref='bids')
    user = db.relationship('UserModel', backref='bids')