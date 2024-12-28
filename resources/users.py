from flask import request, Blueprint, render_template, redirect, url_for, request
from db import db
from models.users import UserModel, Role
from models.goods import GoodModel
from flask_login import login_user, login_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/", methods=["GET", "POST"])
def select_role():
    roles = ["Customs", "Owner", "Buyer"]
    return render_template("index.html")

@users_bp.route('/customs', methods=['GET'])
@login_required
def customs():
    goods = GoodModel.query.all()
    return render_template('customs.html', goods=goods)

#sign up
@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    msg=""
    if request.method == 'POST':
        user = UserModel.query.filter_by(email=request.form['email']).first()
        msg=""
        if user:
            msg="User already exist"
            return render_template('signup.html', msg=msg)
        
        user = UserModel(email=request.form['email'], active=1, password=request.form['password'])
        
        role_id = request.form.get('options')
        role = Role.query.filter_by(id=request.form['options']).first()
        user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        goods=GoodModel.query.all()
        if (role_id == 1):
            return render_template('customs.html', goods=goods)
        elif (role_id == 2):
            return render_template('buyer.html', goods=goods)
        elif (role_id == 3):
            return render_template('owner.html', goods=goods)
        
    else:
        return render_template("signup.html", msg=msg)
    
# signin page
@users_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        user = UserModel.query.filter_by(email=request.form['email']).first()
        if user:
            if  user.password == request.form['password']:
                login_user(user)
                if user.roles:
                    role = user.roles[0].id
                    goods=GoodModel.query.all()
                    if role == 1:
                        return render_template('customs.html', goods=goods)
                    elif role == 2:
                        return render_template('buyer.html', goods=goods)
                    elif role == 3:
                        return render_template('owner.html', goods=goods)
                    else:
                        msg = "User has no role assigned"
            else:
                msg="Wrong password"        
        else:
            msg="User doesn't exist"
        return render_template('signin.html', msg=msg)
    else:
        return render_template("signin.html", msg=msg)