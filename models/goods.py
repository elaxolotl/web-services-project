from db import db

class GoodModel(db.Model):
    __tablename__ = 'goods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    container_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    opening_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), nullable=False)
    guarantee = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    manufacturer_details = db.Column(db.String(200), nullable=True)
    reason_for_detention = db.Column(db.String(200), nullable=True)
    volume = db.Column(db.Float, nullable=True)

    auctions = db.relationship('AuctionModel', back_populates='good')