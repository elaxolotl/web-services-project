from flask import request, abort, jsonify
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from models.goods import Storehouse
from schemas import StoreHouseSchema
from db import db
from flask_security import roles_accepted
from sqlalchemy import case
from datetime import datetime
from flask_login import current_user
from flask_jwt_extended import jwt_required

storehouses_bp = Blueprint('storehouse', __name__, description='operations on storehouses')

@storehouses_bp.route('/storehouses')
class StoreHouses(MethodView):
    
    @jwt_required()
    @roles_accepted("Customs officer")
    #see all storehouses
    def get(self):
        storehouses = Storehouse.query.all()
        storehouse_schema = StoreHouseSchema(many=True)
        return jsonify(storehouse_schema.dump(storehouses))
    
    #add a new storehouse
    @roles_accepted("Customs officer")
    @storehouses_bp.arguments(StoreHouseSchema)
    def post(self, data):
        jwt_required()
        data = request.get_json()
        storehouse = Storehouse(**data)
        try:
            db.session.add(storehouse)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("error: ", e)
            abort(500, description="Error adding container")
        return {"message":"Storehouse added successfully"}