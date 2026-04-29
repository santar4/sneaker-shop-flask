from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from dotenv import load_dotenv
import os
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'app/static/media/'


class Base(DeclarativeBase):
    pass

load_dotenv()
db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from app.models import User, Sneaker, Category, Cart, CartItem

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
target_metadata = db.metadata


with app.app_context():
    db.create_all()
    from app.models import init_categories
    init_categories()


@login_manager.user_loader
def load_user(user_id: int):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    print(user)
    return user

from app.routes import *
from app.filter import *
@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory("media", filename)



