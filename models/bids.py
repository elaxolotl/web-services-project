from db import db

class BidModel(db.Model):
    __tablename__ = 'bids'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)

    good = db.relationship('GoodModel', back_populates='bids')
    
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id']),
        db.ForeignKeyConstraint(['good_id'], ['goods.id']),
    )
