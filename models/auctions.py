from db import db

class AuctionModel(db.Model):
    __tablename__ = 'auction'
    id = db.Column(db.Integer, primary_key=True)
    opening_price = db.Column(db.Float, nullable=False)
    guarantee = db.Column(db.Float, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    good = db.relationship('GoodModel', backref='auction')