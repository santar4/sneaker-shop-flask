from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


def create_mock_data():


    db.session.add()
    db.session.commit()

    print("mock data added")




with app.app_context():
    db.create_all()
    print("Create database")
    create_mock_data()

