from flask import Flask, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from controllers import all_blueprints
from extensions import bcrypt
from models.user import User
from models import db, init_app

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

# Initialize extensions
init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(admin_bp, url_prefix='/admin')
# app.register_blueprint(fhir_bp, url_prefix='/api/fhir')

# Register all blueprints
for blueprint, prefix in all_blueprints:
    app.register_blueprint(blueprint, url_prefix=prefix)
# print(app.url_map)


@app.route('/')
def home():
    return redirect(url_for('auth.login'))


@app.cli.command("create-admin")
def create_admin():
    """Creates an admin user."""
    from getpass import getpass
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    # Check if the username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print("User already in the users table!!!")
    else:
        # If the username does not exist, create a new admin user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(username=username, password=hashed_password, role='admin')
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully")
# # run this command from your terminal "flask create-admin",  to enter the admin’s username and password, hash the password, and store it in the database with the "admin" role.


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)