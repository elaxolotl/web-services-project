from flask import request, abort, Blueprint, jsonify, render_template
from db import db
from models.auctions import AuctionModel
from models.goods import GoodModel
from flask_security import roles_accepted
from flask_login import current_user

auctions_bp = Blueprint('auctions', __name__)

@auctions_bp.route("/goods/<int:good_id>/new-auction", methods=["GET"])
@roles_accepted("Buyer")
def add_auction(good_id):
    msg=""
    good = GoodModel.query.get(good_id)
    if not good:
        abort(404, description="Good not found")
    return render_template("new-auction.html", good=good, msg=msg)


#add new auction
@auctions_bp.route("/goods/<int:good_id>/new-auction", methods=["POST"])
@roles_accepted("Buyer")
def post(good_id):
    msg=""
    data = request.form.to_dict()
    if "value" not in data:
        return render_template("new-auction.html", msg="Missing bet value", good=good)
    data["value"] = float(data["value"])
    good = GoodModel.query.get(good_id)
    if not good:
        return render_template("new-auction.html", msg="Good not found", good=good)
    if data["value"] <= good.opening_price:
        return render_template("new-auction.html", msg="Bet value must be greater than the opening price", good=good)
    new_auction = AuctionModel(
        value=data["value"],
        good_id=good_id,
        user_id=current_user.id
    )
    db.session.add(new_auction)
    db.session.commit()
    goods=GoodModel.query.all()
    return render_template("buyer.html", goods=goods)

#edit auction by id
@auctions_bp.route("/auctions/<int:auction_id>", methods=["PUT"])
@roles_accepted("Buyer")
def put(auction_id):
    data = request.get_json()
    auction = AuctionModel.query.get(auction_id)
    if not auction:
        abort(404, description="Auction not found")
    if "value" not in data:
        abort(400, description="Missing bet value")
    good = GoodModel.query.get(data["good_id"])
    if not good:
        abort(404, description="Good not found")
    if data["value"] <= good.opening_value:
        abort(400, description="Bet value must be greater than the opening value")
    
    auction.value = data["value"]
    auction.user_id = data["user_id"]
    auction.good_id = data["good_id"]
    db.session.commit()
    return jsonify(auction.id), 200

#delete auction by id
@auctions_bp.route("/auctions/<int:auction_id>", methods=["DELETE"])
@roles_accepted("buyer")
def delete(auction_id):
    auction = AuctionModel.query.get(auction_id)
    if not auction:
        abort(404, description="Auction not found")
    db.session.delete(auction)
    db.session.commit()
    return jsonify("Auction deleted"), 200

#see all auctions with the same good id
@auctions_bp.route("/auctions/<int:good_id>", methods=["GET"])
@roles_accepted("buyer", "owner", "customs")
def get(good_id):
    auctions = AuctionModel.query.filter_by(good_id=good_id).all()
    return jsonify([auction.id for auction in auctions])