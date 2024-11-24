# controllers/admin_controller.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from services import create_user, check_user_exists
from models import db
from models.user import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_page():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('auth.dashboard'))
    return render_template('admin.html')

@admin_bp.route('/view_users')
@login_required
def view_users():
    # Logic to view users
    return "View Users Page"

@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    # Logic to create user
    return "Create User Page"

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Logic to delete user
    return f"User {user_id} deleted"