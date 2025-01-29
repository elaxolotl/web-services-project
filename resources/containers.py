from flask import request, abort, jsonify, make_response
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from models.goods import ContainerModel
from schemas import ContainerSchema
from db import db
from flask_security import roles_accepted
from flask_jwt_extended import jwt_required

containers_bp = Blueprint('containers', __name__, description='operations on containers')


@containers_bp.route('/containers')
class Containers(MethodView):
    
    #add a new container
    @containers_bp.doc(security=[{"BearerAuth": []}])
    @roles_accepted("Customs officer")
    @containers_bp.arguments(ContainerSchema)
    @containers_bp.response(201, ContainerSchema)
    def post(self, container_data):
        jwt_required()
        container_data = request.get_json()
        existing_container = ContainerModel.query.filter_by(id=container_data['id']).first()
        if existing_container:
            response = make_response(jsonify({"message": "Container with this ID already exists"}), 400)
            return response
        container = ContainerModel(**container_data)
        try:
            db.session.add(container)
            db.session.commit()
        except SQLAlchemyError as e:
            print("error: ", e)
            abort(500, description="Error adding container")
        return container
        
    #see all containers
    @roles_accepted("Customs officer")
    def get(self):
        jwt_required()
        containers = ContainerModel.query.all()
        containers_schema = ContainerSchema(many=True)
        return jsonify(containers_schema.dump(containers))
    
@containers_bp.route('/containers/<string:container_id>', methods=['GET'])
@roles_accepted("Customs officer")
def get(container_id):
    jwt_required()
    container = ContainerModel.query.get_or_404(container_id)
    container_schema = ContainerSchema()
    return jsonify(container_schema.dump(container))

@containers_bp.route('/containers/<string:container_id>', methods=['PUT'])
@roles_accepted("Customs officer")
def update_container(container_id):
    jwt_required()
    container = ContainerModel.query.get_or_404(container_id)
    data = request.get_json()
    if 'address' in data:
        container.address = data['address']
    if 'latitude' in data:
        container.latitude = data['latitude']
    if 'longitude' in data:
        container.longitude = data['longitude']
    db.session.commit()
    container_schema = ContainerSchema()
    return jsonify(container_schema.dump(container))
