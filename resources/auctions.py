from flask import request, jsonify, abort
from flask_smorest import Blueprint
from models.goods import Auction
from models.goods import GoodModel
from schemas import AuctionSchema
from db import db
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_security import roles_accepted
from sqlalchemy.exc import SQLAlchemyError

auctions_bp = Blueprint('auctions', __name__, description="Operations on auctions")

@auctions_bp.route("/auctions")
class Auctions(MethodView):
    
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    @auctions_bp.arguments(AuctionSchema)
    @auctions_bp.response(201, AuctionSchema)
    def post(self, auction_data):
        auction_data = request.get_json()
        new_auction = Auction(**auction_data)
        try:
            db.session.add(new_auction)
            db.session.commit()
        except SQLAlchemyError as e:
            print("error: ", e)
            abort(500, description="Error adding auction")
        return new_auction
    
    @auctions_bp.response(200, AuctionSchema(many=True))
    def get(self):
        return Auction.query.all()

@auctions_bp.route("/auctions/<int:auction_id>")
class AuctionDetail(MethodView):
    
    @auctions_bp.response(200, AuctionSchema())
    def get(self, auction_id):
        return Auction.query.get_or_404(auction_id)
    
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def delete(self, auction_id):
        jwt_required()
        auction = Auction.query.get_or_404(auction_id)
        db.session.delete(auction)
        db.session.commit()
        return {"message": "Auction deleted"}
    
    @auctions_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def put(self, auction_id):
        jwt_required()
        auction_data = request.get_json()
        auction = Auction.query.get_or_404(auction_id)
        schema = AuctionSchema(partial=True)
        updated_data = schema.load(auction_data)
        for key, value in updated_data.items():
            setattr(auction, key, value)
        db.session.commit()
        return {"message": "Auction updated successfully"}