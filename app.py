from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'novacares-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novacares.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bank_name = db.Column(db.String(150))
    account_number = db.Column(db.String(50))
    account_name = db.Column(db.String(150))
    
class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')
    
class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    bank_name = db.Column(db.String(150))
    account_number = db.Column(db.String(50))
    account_name = db.Column(db.String(150))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/settings', methods
