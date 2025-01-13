from db import db
from flask_security import UserMixin, RoleMixin
import uuid

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    name = db.Column(db.String(80), nullable=False)
    national_id = db.Column(db.Integer, unique=True, nullable=True)
    fiscal_id = db.Column(db.String(8), unique=True, nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    active = db.Column(db.Boolean())

    roles = db.relationship('Role', secondary=roles_users, backref='roled')

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)