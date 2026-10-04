"""School district application. Students: Brooke Andrie; add teammates before submission."""
import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

root = Path(__file__).resolve().parents[2]
app = Flask(__name__, template_folder=str(root / 'templates'), static_folder=str(root / 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'local-development-key-change-for-deployment')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///schools.db')
from flask_wtf.csrf import CSRFProtect
CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from app import models
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(models.User, user_id)

from app import routes
