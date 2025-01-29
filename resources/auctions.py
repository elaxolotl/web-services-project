from flask import request, abort
from flask_smorest import Blueprint
from models.auctions import AuctionModel
from models.goods import GoodModel
from schemas import AuctionSchema
from db import db
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import asyncio
from models.users import UserModel, Buyer
from notifications import send_notification

auctions_bp = Blueprint('auctions', __name__, description="Operations on auctions")

@auctions_bp.route("/goods/<int:good_id>/auction")
class Auction(MethodView):
    
    #place new auction
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    @auctions_bp.arguments(AuctionSchema)
    @auctions_bp.response(201, AuctionSchema)
    def post(self, auction_data, good_id):
        jwt_required()
        auction_data = request.get_json()
        good = GoodModel.query.get(good_id)
        good.status = "on_sale"
        auction_data["good_id"] = good.id
        if "end_date" in auction_data:
            auction_data["end_date"] = datetime.fromisoformat(auction_data["end_date"].replace("Z", "+00:00"))
        new_auction = AuctionModel(**auction_data)
        try:
            db.session.add(new_auction)
            db.session.commit()
            buyers = UserModel.query.join(Buyer).all()
            for buyer in buyers:
                asyncio.run(send_notification(buyer.id, buyer.email, buyer.number, "A new auction has been created", new_auction.id))
        except SQLAlchemyError as e:
            print("error: ", e)
            abort(500, description="Error adding auction")
        return new_auction

@auctions_bp.route("/auctions/<int:auction_id>")
class AuctionDetail(MethodView):
    
    #see an auction based on id
    @auctions_bp.response(200, AuctionSchema())
    def get(self, auction_id):
        return AuctionModel.query.get_or_404(auction_id)
    
    #delete an auction
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def delete(self, auction_id):
        jwt_required()
        auction = AuctionModel.query.get_or_404(auction_id)
        db.session.delete(auction)
        db.session.commit()
        return {"message": "Auction deleted"}
    
    #update an auction
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def put(self, auction_id):
        jwt_required()
        auction_data = request.get_json()
        auction = AuctionModel.query.get_or_404(auction_id)
        schema = AuctionSchema(partial=True)
        updated_data = schema.load(auction_data)
        for key, value in updated_data.items():
            setattr(auction, key, value)
        db.session.commit()
        return {"message": "Auction updated successfully"}