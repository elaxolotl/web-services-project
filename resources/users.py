from flask import jsonify, current_app
from flask_smorest import Blueprint
from schemas import UserSignupSchema, UserLoginSchema
from models.users import UserModel, Role
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import datetime
import jwt
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__, description="Operations on users")

#signup user
@users_bp.route('/signup', methods=["POST"])
@users_bp.arguments(UserSignupSchema)
@users_bp.response(201, UserSignupSchema)
def signup(data):
    data['email'] = data['email'].lower()
    if UserModel.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400
    if data["role_id"]==2:
        if not data["national_id"] and not data["fiscal_id"]:
            return jsonify({"error": "Please provide a national ID or a fiscal ID"}), 400
    data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
    user = UserModel(email=data['email'].lower(), password=data['password'], name=data["name"], national_id=data['national_id'], fiscal_id=data['fiscal_id'], active=1)
    role = Role.query.filter_by(id=data['role_id']).first()
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    expiration = datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
    token = jwt.encode(
        {"sub": str(user.id), "exp": expiration},
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return jsonify({"message": "Signup successful", "token": token})

#login user
@users_bp.route('/login', methods=['POST'])
@users_bp.arguments(UserLoginSchema)
def login(data):
    user = UserModel.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        expiration = datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
        token = jwt.encode({"sub": str(user.id), "exp": expiration},
        current_app.config['SECRET_KEY'],
        algorithm="HS256")
        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 400

#check current user
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.route('/user', methods=['GET'])
@jwt_required()
def load_user():
    return jsonify({"email": current_user.email, "role": current_user.roles[0].name})

#logout
@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200