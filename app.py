from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from controllers import all_blueprints
from extensions import bcrypt
from models.user import User
from models import db

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(admin_bp, url_prefix='/admin')
# Register all blueprints

for blueprint, prefix in all_blueprints:
    app.register_blueprint(blueprint, url_prefix=prefix)


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


# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from flask_migrate import Migrate

# app = Flask(__name__, template_folder='templates')
# app.config['SECRET_KEY'] = 'Zhouyi_CSCI6180'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhouyi1995@localhost/visualization1'

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# # # Set up Flask-Migrate with the app and database
# # migrate = Migrate(app, db)  # Add this line to set up Flask-Migrate

# # Define the User model
# class User(db.Model, UserMixin):
#     __tablename__ = 'users' # Specifies the table name in visualization1 database
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     role = db.Column(db.String(50), nullable=False, default='common')


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route('/')
# def home():
#     return redirect(url_for("login"))

# @app.route('/signup',methods = ['GET','POST'])
# def signup():
#     session.clear()
#     if request.method =='POST':
#         username = request.form['username']
#         password = request.form['password']
#         # role = request.form['role']  # Get the selected role
#         role = 'common'
    
#         #check if username exists
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists','danger')
#             return redirect(url_for('login'))
    
#         #Hash password and save new user
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(username = username, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('Account created successfully!', 'success')
#         return redirect(url_for('login'))
    
#     return render_template('signup.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     session.clear()
#     # if current_user.is_authenticated:
#     #     if current_user.role == 'admin':
#     #         return redirect(url_for('admin_page'))
#     #     else:
#     #         return redirect(url_for('dashboard'))
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()

#         if user and bcrypt.check_password_hash(user.password, password):
#             login_user(user)
#             flash('Login successful!', 'success')
#             if user.role == 'admin':
#                 return redirect(url_for('admin_page'))
#             else:
#                 return redirect(url_for('dashboard'))
        
#         flash('Invalid username or password.', 'danger')

#     return render_template('login.html')


# @app.route('/admin')
# @login_required
# def admin_page():
#     if current_user.role != 'admin':
#         flash('You do not have permission to access this page.', 'danger')
#         return redirect(url_for('dashboard'))  # Redirect to a different page
#     # # Example statistics calculations
#     # total_users = User.query.count()
#     # active_users = User.query.filter_by(active=True).count()  # Assuming there's an 'active' column

#     return render_template('admin.html')
#     # return render_template('admin.html', total_users=total_users, active_users=active_users)

# @app.route('/view_users')
# @login_required
# def view_users():
#     # Logic for viewing users
#     return "View Users Page"

# @app.route('/create_user', methods=['GET', 'POST'])
# @login_required
# def create_user():
#     # Logic for creating a user
#     return "Create User Page"

# @app.route('/delete_user/<int:user_id>', methods=['POST'])
# @login_required
# def delete_user(user_id):
#     # Logic for deleting a user
#     return f"User {user_id} deleted"

# # Dashboard route (requires login)
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')




# # Logout route
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     session.clear()
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))


# @app.route('/feature1')
# @login_required
# def feature1():
#     return "<h1>Feature 1 Page</h1>"

# @app.route('/feature2')
# @login_required
# def feature2():
#     return "<h1>Feature 2 Page</h1>"

# @app.route('/feature3')
# @login_required
# def feature3():
#     return "<h1>Feature 3 Page</h1>"


# # Run the app
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Create tables if they don't exist
#     app.run(debug=True)

#/signup URL: To access signup.html, go to http://127.0.0.1:5000/signup
#/login URL: To access login.html, go to http://127.0.0.1:5000/login