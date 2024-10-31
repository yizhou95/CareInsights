from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'Zhouyi_CSCI6180'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zhouyi1995@localhost/visualization1'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User model
class User(db.Model, UserMixin):
    __tablename__ = 'users' # Specifies the table name in visualization1 database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
    
        #check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists','danger')
            return redirect(url_for('signup'))
    
        #Hash password and save new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username = username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

# Dashboard route (requires login)
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! Welcome to your dashboard.'

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

#/signup URL: To access signup.html, go to http://127.0.0.1:5000/signup
#/login URL: To access login.html, go to http://127.0.0.1:5000/login