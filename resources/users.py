from flask import jsonify, request, current_app
from flask_smorest import Blueprint
from schemas import UserSignupSchema, UserLoginSchema
from models.users import UserModel, Role
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import datetime
import jwt
from functools import wraps
from flask_login import login_user

users_bp = Blueprint('users', __name__, description="Operations on users")

#verify token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': "Token is missing"}), 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = UserModel.query.filter_by(id=data['user']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': "Expired token"}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': "Invalid token"}), 403
        return f(current_user, *args, **kwargs)
    return decorated

#signup user
@users_bp.route('/signup', methods=["POST"])
@users_bp.arguments(UserSignupSchema)
@users_bp.response(201, UserSignupSchema)
def signup(data):
    data['email'] = data['email'].lower()
    if UserModel.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400
    if data["role_id"]==2:
        if "national_id" not in data and not "fiscal_id" not in data:
            return jsonify({"error": "Please provide a national ID or a fiscal ID"}), 400
    data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256')
    user = UserModel(email=data['email'].lower(), password=data['password'], name=data["name"], national_id=data['national_id'], fiscal_id=data['fiscal_id'], active=1)
    role = Role.query.filter_by(id=data['role_id']).first()
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    token = jwt.encode({'user' : user.id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, current_app.config["SECRET_KEY"])
    return jsonify({"message": "Signup successful", "token": token})

#login user
@users_bp.route('/login', methods=['POST'])
@users_bp.arguments(UserLoginSchema)
def login(data):
    user = UserModel.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        token = jwt.encode({'user' : user.id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, current_app.config["SECRET_KEY"])
        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 400

#check current user
@users_bp.route('/user', methods=['GET'])
@token_required
def load_user(current_user):
    return jsonify({"email": current_user.email, "role": current_user.roles[0].name})
