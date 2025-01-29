from flask import request, jsonify
from flask_smorest import Blueprint
from db import db
from schemas import BidSchema
from models.bids import BidModel
from models.auctions import AuctionModel
from models.users import UserModel
from flask_security import roles_accepted
from flask_login import current_user
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from datetime import datetime
from notifications import send_notification
import asyncio

bids_bp = Blueprint('bids', __name__, description="Operations on bids")
@bids_bp.route("/auctions/<int:auction_id>/bids")
class Bids(MethodView):
    
    #place a bid in an auction
    @bids_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Buyer")
    @bids_bp.response(201)
    def post(self, auction_id):
        jwt_required()
        data = request.get_json()
        auction = AuctionModel.query.filter_by(id=auction_id).first()
        if not auction:
            return {"message": "Auction not found."}, 404
        if data['value'] <= auction.opening_price:
            return {"message": f"Bid value must be higher than {auction.opening_price}."}, 400
        highest_bid = BidModel.query.filter_by(auction_id=auction_id).order_by(BidModel.value.desc()).first()
        data['user_id']=current_user.id
        data['auction_id']=auction_id
        data["created_at"]=datetime.utcnow()
        bid = BidModel(**data)
        db.session.add(bid)
        db.session.commit()
        new_highest_bid = BidModel.query.filter_by(auction_id=auction_id).order_by(BidModel.value.desc()).first()
        if highest_bid and new_highest_bid and highest_bid.id != new_highest_bid.id:
            previous_winner = UserModel.query.get(highest_bid.user_id)
            asyncio.run(send_notification(previous_winner.email, previous_winner.email, previous_winner.number, "Your bid has lost its first place! reclaim it by placing anoter bid", bid.id))
        return jsonify({"message": "Bid placed."}), 201
    
    #get all bids for a specific auction ordered from highest to lowest
    @bids_bp.doc(security=[{"BearerAuth": []}])    
    @roles_accepted("Buyer")
    @bids_bp.response(200, BidSchema(many=True))
    def get(self, auction_id):
        jwt_required()
        bids = BidModel.query.filter_by(auction_id=auction_id).order_by(BidModel.value.desc()).all()
        if not bids:
            return {"message": "No bids placed for this auction."}, 404
        return bids


@bids_bp.route("/bids/<int:bid_id>")
class Bid(MethodView):
    
    #see all the details of a specific bid
    @bids_bp.doc(security=[{"BearerAuth": []}])
    @bids_bp.response(200, BidSchema())
    def get(self, bid_id):
        jwt_required()
        return BidModel.query.get_or_404(bid_id)
    
    #delete a bid
    @bids_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Buyer")
    def delete(self, bid_id):
        jwt_required()
        if current_user.id != BidModel.query.get_or_404(bid_id).user_id:
            return {"message": "You can only delete your own bids."}, 400
        bid = BidModel.query.get_or_404(bid_id)
        db.session.delete(bid)
        db.session.commit()
        return {"message": "Bid deleted"}