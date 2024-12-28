from db import db
from models.users import UserModel
from models.goods import GoodModel

class AuctionModel(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)

    good = db.relationship('GoodModel', back_populates='auctions')
    
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id']),
        db.ForeignKeyConstraint(['good_id'], ['goods.id']),
    )
