# models/user.py
from models import db
from flask_login import UserMixin
from extensions import bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='common')

    # Method to set password, which automatically hashes it
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password, method="pbkdf2:sha256")
    
    # Method to check the hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)