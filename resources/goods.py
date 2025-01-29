from flask import request, abort, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from models.goods import GoodModel
from models.auctions import AuctionModel
from schemas import GoodSchema
from db import db
from flask_security import roles_accepted
from sqlalchemy import case
from datetime import datetime
from flask_login import current_user
from flask_jwt_extended import jwt_required


goods_bp = Blueprint('goods', __name__, description="Operations on detained goods")

@goods_bp.route("/goods")
class Goods(MethodView):
    
    #add a new detained good
    @goods_bp.doc(security=[{"BearerAuth": []}])
    @jwt_required()
    @roles_accepted("Customs officer")
    @goods_bp.arguments(GoodSchema)
    @goods_bp.response(201, GoodSchema)
    def post(self, good_data):
        good_data = request.get_json()
        good_data["customs_officer_id"]=current_user.id
        if "expiry_date" in good_data and good_data["expiry_date"]:
            good_data["expiry_date"] = datetime.strptime(good_data["expiry_date"], "%Y-%m-%d").date()
        if good_data.get("perishable") and not good_data.get("expiry_date"):
            return jsonify({"error":"Expiry date must be provided for perishable goods"}), 400
        new_good = GoodModel(**good_data)
        try:
            db.session.add(new_good)
            db.session.commit()
        except SQLAlchemyError as e:
            print("error: ", e)
            abort(500, description="Error adding good")
        return new_good
    
    #get all detained goods
    @goods_bp.response(200, GoodSchema(many=True))
    def get(self):
        status_filter = request.args.get('status', None)
        query = GoodModel.query.order_by(
            case(
                (GoodModel.perishable == True, 0),
                else_=1
            ).asc(),
            GoodModel.expiry_date.asc().nulls_last(),
            GoodModel.created_at.asc()
        )
        if status_filter and status_filter in ["detained", "on_sale", "sold", "no_commercial_value"]:
            query = query.filter(GoodModel.status == status_filter)
        return query.all()

@goods_bp.route("/goods/<int:good_id>")
class Good(MethodView):
    
    #see a specific detained good
    @goods_bp.response(200, GoodSchema())
    def get(self, good_id):
        return GoodModel.query.get_or_404(good_id)
    
    #delete a detained good
    @goods_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def delete(self, good_id):
        jwt_required()
        good_id = request.view_args['good_id']
        good = GoodModel.query.get_or_404(good_id)
        AuctionModel.query.filter_by(good_id=good_id).delete()     
        db.session.delete(good)
        db.session.commit()
        return {"message": "Good deleted"}
    
    #edit a detained good
    @goods_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    def put(self, good_id):
        jwt_required()
        good_data = request.get_json()
        good = GoodModel.query.get_or_404(good_id)
        schema = GoodSchema(partial=True)
        updated_data=schema.load(good_data)
        for key, value in updated_data.items():
            setattr(good, key, value)
        db.session.commit()
        return {"message": "Detained good updated succesfully"}