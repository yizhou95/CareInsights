# services/user_service.py
from models.user import User
from models import db
from extensions import bcrypt

def create_user(username, password, role='common'):
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    """
    Retrieves a user from the database by username.
    """
    return User.query.filter_by(username=username).first()


def check_user_exists(username):
    return User.query.filter_by(username=username).first() is not None

def verify_password(user, password):
    """
    Verifies a user's password by comparing it with the hashed password in the database.
    """
    return bcrypt.check_password_hash(user.password, password)