# controllers/admin_controller.py
from flask import Blueprint, render_template, flash, redirect, url_for,request
from flask_login import login_required, current_user
from services import create_user, check_user_exists
from models import db
from models.user import User
from models.json_processor  import process_fhir_resource
from models.csv_processor import process_csv_file
import json

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

@admin_bp.route('/upload_csv', methods=['GET', 'POST'])
def upload_file_csv():
    if request.method == 'POST':
        # Handle CSV file upload
        if 'single_csv_file' in request.files:
            csv_file = request.files['single_csv_file']
            file_name = csv_file.filename  # Get the file name
            if csv_file and file_name.endswith('.csv'):
                try:
                    # Read the content of the CSV file
                    file_content = csv_file.read().decode('utf-8')

                    # Call the process_csv_file method to handle the file
                    process_csv_file(file_name, file_content)

                    # Redirect with a success message after processing
                    flash(f"Successfully processed file: {file_name}", "success")
                    return redirect(url_for('admin.upload_file_csv'))  # Redirect to /admin/upload_csv
                except Exception as e:
                    flash(f"Error processing file '{file_name}': {str(e)}", "danger")
                    return redirect(url_for('admin.upload_file_csv'))  # Redirect to /admin/upload_csv
            else:
                flash("Invalid CSV file format", "danger")
                return redirect(url_for('admin.upload_file_csv'))  # Redirect to /admin/upload_csv

        flash("No file uploaded", "danger")
        return redirect(url_for('admin.upload_file_csv'))  # Redirect to /admin/upload_csv

    return render_template('upload_csv.html')  # Render upload page for GET request
@admin_bp.route('/upload_json', methods=['GET', 'POST'])
def upload_file_json():
    if request.method == 'POST':
        # Handle JSON file upload
        if 'single_json_file' in request.files:
            json_file = request.files['single_json_file']
            if json_file and json_file.filename.endswith('.json'):
                try:
                    # Load and process the JSON data
                    json_data = json.load(json_file)
                    process_fhir_resource(json_data)

                    # Redirect with a success message after processing
                    flash(f"Successfully processed file: {json_file.filename}", "success")
                    return redirect(url_for('admin.upload_file_json'))  # Redirect to /admin/upload_csv
                except Exception as e:
                    flash(f"Error processing file '{json_file}': {str(e)}", "danger")
                    return redirect(url_for('admin.upload_file_json'))  # Redirect to /admin/upload_csv
            else:
                    flash("Invalid JSON file format", "danger")
                    return redirect(url_for('admin.upload_file_json'))  # Redirect to /admin/upload_csv

        flash("No file uploaded", "danger")
        return redirect(url_for('admin.upload_file_json'))  # Redirect to /admin/upload_csv
    return render_template('upload_json.html')  # Render upload page for GET request
