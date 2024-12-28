from flask import request, abort, Blueprint, jsonify, render_template
from db import db
from models.goods import GoodModel
from models.users import UserModel
from flask_security import roles_accepted

goods_bp = Blueprint('goods', __name__)

@goods_bp.route("/new-good", methods=["GET"])
@roles_accepted("Customs officer")
def add_detained_good():
    return render_template("new-good.html")

#add new good
@goods_bp.route("/goods", methods=["POST"])
@roles_accepted("Customs officer") 
def post():
    good_data = request.form.to_dict()
    required_fields = [
        "name", "container_id", "quantity", "opening_price",  
        "status", "guarantee"
    ]

    missing_fields = [field for field in required_fields if field not in good_data]

    if missing_fields:
        abort(400, description="Missing fields: {}".format(", ".join(missing_fields)))
        
    def sanitize(value):
        return value if value != '' else None

    new_good = GoodModel(
        name=good_data.get("name"),
        container_id=good_data.get("container_id"),
        quantity=sanitize(good_data.get("quantity")),
        opening_price=sanitize(good_data.get("opening_price")),
        status=good_data.get("status"),
        guarantee=good_data.get("guarantee"),
        description=sanitize(good_data.get("description")),
        category=sanitize(good_data.get("category")),
        manufacturer_details=sanitize(good_data.get("manufacturer_details")),
        reason_for_detention=sanitize(good_data.get("reason_for_detention")),
        volume=sanitize(good_data.get("volume"))
    )
    
    db.session.add(new_good)
    db.session.commit()
    
    goods=GoodModel.query.all()
        
    return render_template("goods.html", goods=goods)

#get good by id
@goods_bp.route("/goods/<int:good_id>", methods=["GET"])
def get_by_id(good_id):
    good = GoodModel.query.get(good_id)
    if not good:
        abort(404, description="Good not found")
    
    return jsonify(good.id), 200

#see all goods
@goods_bp.route("/goods", methods=["GET"])
def get():
    goods = GoodModel.query.all()
    return render_template("goods.html", goods=goods)

#delete good by id
@goods_bp.route("/goods/<int:good_id>", methods=["DELETE"])
@roles_accepted("Customs officer")
def delete(good_id):
    good = GoodModel.query.get(good_id)
    if not good:
        abort(404, description="Good not found")
    
    db.session.delete(good)
    db.session.commit()
    
    return jsonify("Good deleted"), 200

#update good by id
@goods_bp.route("/goods/<int:good_id>", methods=["PUT"])
@roles_accepted("Customs officer")
def put(good_id):
    data = request.get_json()
    good = GoodModel.query.get(good_id)
    
    if not good:
        abort(404, description="Good not found")
    
    if 'name' in data:
        good.name = data['name']
    if 'price' in data:
        good.price = data['price']
    if 'description' in data:
        good.description = data['description']
    if "opening_price" in data:
        good.opening_price = data["opening_price"]
    if "status" in data:
        good.status = data["status"]
    if "guarantee" in data:
        good.guarantee = data["guarantee"]
    
    db.session.commit()
    
    return jsonify(good.name), 200
    