from flask import request
from flask_smorest import Blueprint
from db import db
from models.bids import BidModel
from flask_security import roles_accepted
from flask_login import current_user
from flask_security import roles_accepted
from flask.views import MethodView
from schemas import BidSchema
from resources.users import token_required
from models.goods import GoodModel
auctions_bp = Blueprint('auctions', __name__, description="Operations on auctions")

@auctions_bp.route("/goods/<int:good_id>/bids")
class Bids(MethodView):
    
    #place a bid on a specific good
    @token_required
    @roles_accepted("Buyer")
    @auctions_bp.arguments(BidSchema)
    @auctions_bp.response(201, BidSchema)
    def post(self, good_id):
        data = request.get_json()
        good = GoodModel.query.get(good_id)
        if not good:
            return {"message": "Good not found."}, 404
        if good["status"]!="on_sale":
            return {"message": "This good is not on sale."}, 400
        if data['value'] <= good.opening_price:
            return {"message": f"Bid value must be higher than {good.opening_price}."}, 400
        data['user_id']=current_user.id
        data['good_id']=good_id
        data['value']=data['value']
        bid = BidModel(**data)
        return bid
    
    #get all bids for a specific good ordered from highest to lowest
    @token_required
    @roles_accepted("Buyer")
    @auctions_bp.response(200, BidSchema(many=True))
    def get(self, good_id):
        bids = BidModel.query.filter_by(good_id=good_id).order_by(BidModel.value.desc()).all()
        if not bids:
            return {"message": "No bids placed for this good."}, 404
        return bids


@auctions_bp.route("/bids/<int:bid_id>")
class Bid(MethodView):
    
    #see all the details of a specific bid
    @token_required
    @auctions_bp.response(200, BidSchema())
    def get(self, bid_id):
        return BidModel.query.get_or_404(bid_id)
    
    #delete a bid
    @token_required
    @roles_accepted("Buyer")
    def delete(self, bid_id):
        if current_user.id != BidModel.query.get_or_404(bid_id).user_id:
            return {"message": "You can only delete your own bids."}, 400
        bid = BidModel.query.get_or_404(bid_id)
        db.session.delete(bid)
        db.session.commit()
        return {"message": "Bid deleted"}