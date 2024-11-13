# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from services import create_user, check_user_exists
from models.user import User
from models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'common'
        
        if check_user_exists(username):
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.login'))
        
        create_user(username, password, role)
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_page') if user.role == 'admin' else url_for('auth.dashboard'))
        
        flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))



@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@auth_bp.route('/feature1')
@login_required
def feature1():
    return "<h1>Feature 1 Page</h1>"

@auth_bp.route('/feature2')
@login_required
def feature2():
    return "<h1>Feature 2 Page</h1>"

@auth_bp.route('/feature3')
@login_required
def feature3():
    return "<h1>Feature 3 Page</h1>"