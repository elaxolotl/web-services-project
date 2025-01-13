from flask import Flask, render_template, Blueprint, send_from_directory
from flask_smorest import Blueprint

frontend_bp = Blueprint('frontend', __name__, template_folder='templates')

@frontend_bp.route('/')
def landing_page():
    return render_template('index.html')

@frontend_bp.route('/features')
def landing_page():
    return render_template('features.html')