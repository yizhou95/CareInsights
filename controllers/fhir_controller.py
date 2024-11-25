# controllers/fhir_controller.py
from flask import Blueprint, render_template, jsonify
from models.user import User
from models import db
from sqlalchemy import Table, MetaData

fhir_bp = Blueprint('fhir', __name__)

table_columns = {
    "patients": ["Id", "FIRST","LAST","BIRTHDATE", "RACE", "GENDER","ADDRESS","CITY","STATE","COUNTY","ZIP","HEALTHCARE_EXPENSES","HEALTHCARE_COVERAGE"],
    "organizations": ["Id", "NAME", "ADDRESS","CITY","STATE","ZIP","PHONE"],
    "providers":["Id","ORGANIZATION", "NAME", "GENDER","SPECIALITY","ADDRESS","CITY","STATE","ZIP"],
    "supplies": ["DATE","PATIENT","ENCOUNTER","CODE","DESCRIPTION","QUANTITY","ID"],
    "allergies": ["START","STOP","PATIENT","ENCOUNTER","CODE","SYSTEM1","DESCRIPTION","TYPE","CATEGORY","DESCRIPTION1","SEVERITY1","DESCRIPTION2","SEVERITY2","ID"],
    "careplans": ["Id","START","STOP","PATIENT","ENCOUNTER","CODE","DESCRIPTION","REASONCODE","REASONDESCRIPTION"],
}


@fhir_bp.route('/<table_name>', methods=['GET'])
def get_table_data(table_name):
    # print(f"Received request for table: {table_name}")
    # Logic to fetch data dynamically from a specified table
    metadata = MetaData()
    try:
        if table_name not in table_columns:
            return jsonify({"error": f"Table '{table_name}' is not allowed or not configured."}), 400
        # Reflect the table from the database
        table = Table(table_name, metadata, autoload_with=db.engine)
        # print(f"Columns in '{table_name}' table: {table.columns.keys()}")  # Debug log
        
        # Dynamically validate and fetch only specified columns
        valid_columns = [col for col in table_columns[table_name] if col in table.columns.keys()]
        if not valid_columns:
            return jsonify({"error": f"No valid columns found for table '{table_name}'"}), 400
        
        # print(f"Valid columns for query: {valid_columns}")  # Debug log
        # Get only the specified columns
        columns_to_query = [table.c[column] for column in valid_columns]

        # Query all data from the table
        query = db.session.query(*columns_to_query).all()
        # Debug log for query results
        # print(f"Query Result for {table_name}: {query}")
        
        # Convert query result to a list of dictionaries
        data = [{column: getattr(row, column) for column in valid_columns} for row in query]
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data for table '{table_name}': {e}")
        return jsonify({"error": f"Table '{table_name}' not found or inaccessible.", "details": str(e)}), 500
        