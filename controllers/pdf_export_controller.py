# controllers/pdf_export_controller.py
from flask import Blueprint, render_template, flash
from services import create_user, check_user_exists
from models import db
from models.user import User
from flask import jsonify, request
from sqlalchemy import Table, MetaData, text
from fpdf import FPDF
import polars as pl
from services import PDF
import pandas as pd

pdf_bp = Blueprint('/pdf', __name__)


def get_report_data(patient_id):
    try:
        # Call the first stored procedure
        result1 = db.session.execute(
            text("CALL genreport(:patient_id)"), 
            {"patient_id": patient_id}
        )
        # Convert to a list of tuples
        results1 = [tuple(row) for row in result1.fetchall()]

        # Call the second stored procedure
        result2 = db.session.execute(
            text("CALL procobserve(:patient_id)"), 
            {"patient_id": patient_id}
        )
        # Convert to a list of tuples
        results2 = [tuple(row) for row in result2.fetchall()]

        # Return both results
        return [results1, results2]

    except Exception as e:
        # Handle errors (e.g., logging)
        print(f"Error while fetching report data: {e}")
        return None

def generate_pdf(data, filename='report.pdf'):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    
    # Add report title
    pdf.cell(200, 10, 'Patient Report', ln=True, align='C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Patient Demographics', ln=True, align='L')

    df = pl.DataFrame(data[1], schema=['Id', 'PROCEDUREDESCR', 'PROCSTART', 'PROCSTOP', 'OBSERVEDATE', 'CATEGORY', 'OBSERVATION', 'VALUE', 'TYPE'], orient='row')
    df2 = pl.DataFrame(data[0], schema=['Id', 'FIRST', 'LAST', 'BIRTHDATE', 'GENDER', 'RACE', 'ETHNICITY', 'ALLERGY', 'ASTART', 'AEND', 'CAREPLAN', 'CAREDESCRIPTION', 'CARESTART', 'CAREEND', 'CONDITION', 'CONDSTART', 'CONDEND', 'MEDICINE', 'REASON', 'MEDSTART', 'MEDEND', 'IMMUNIZATION', 'IMMDATE'], orient='row')

    result = df2.group_by("FIRST").agg([
    pl.col("LAST").first().alias("Last Name"),
    pl.col("BIRTHDATE").first().alias("BIRTHDATE"),
    pl.col("GENDER").first().alias("GENDER"),
    pl.col("RACE").first().alias("RACE"),
    pl.col("ETHNICITY").first().alias("ETHNICITY"),
    ])
    
    columns = ["FIRST", 'Last Name', 'BIRTHDATE', 'GENDER', 'RACE', 'ETHNICITY']
    data = result.to_pandas().to_dict(orient="records")
    for col in columns:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, col + ": ", border=0, align="L") 
        pdf.set_font('Arial', '', 10)
        pdf.cell(40, 10, data[0][col] , border=0, align="L")
        pdf.ln()

###########
#    Tables
###########
    # Condition Table ------------------------------------
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Patient Conditions', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    result = df2.group_by("CONDITION").agg([
    pl.col("CONDSTART").first().alias("Start_Date"),
    pl.col("CONDEND").first().alias("End_Date")
    ])

    data = result.to_pandas().to_dict(orient="records")

    headers = ["CONDITION", "Start_Date", "End_Date"]

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Conditions",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    # Allergy Table ------------------------------------
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Patient Allergies', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ['ALLERGY', 'Start_Date', 'End_Date']
    result = df2.group_by("ALLERGY").agg([
    pl.col("ASTART").first().alias("Start_Date"),
    pl.col("AEND").first().alias("End_Date")
    ])
    data = result.to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Allergies",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    #  CarePlan Table ------------------------------
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Patient CarePlan', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ['CAREPLAN', 'Reason', 'Start_Date', 'End_Date']
    result = df2.group_by("CAREPLAN").agg([
    pl.col("CAREDESCRIPTION").first().alias("Reason"),
    pl.col("CARESTART").first().alias("Start_Date"),
    pl.col("CAREEND").first().alias("End_Date")
    ])
    data = result.to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No CarePlan",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    # Medicine Table
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Medications', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ['MEDICINE', 'Reason', 'Start_Date', 'End_Date']
    result = df2.group_by("MEDICINE").agg([
    pl.col("REASON").first().alias("Reason"),
    pl.col("MEDSTART").first().alias("Start_Date"),
    pl.col("MEDEND").first().alias("End_Date")
    ])
    data = result.to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Medicine",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    # Immunization Table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Immunizations', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ["IMMUNIZATION", 'Date']
    result = df2.group_by("IMMUNIZATION").agg([
    pl.col("IMMDATE").first().alias("Date"),
    ])
    data = result.to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Immunizations",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    # Procedure Table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Procedures', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ['PROCEDUREDESCR', 'Start_Date', 'End_Date']
    result = df.group_by("PROCEDUREDESCR").agg([
    pl.col("PROCSTART").first().alias("Start_Date"),
    pl.col("PROCSTOP").first().alias("End_Date"),
    ])
    data = result.to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Procedures",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    # Observation Table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 10, 'Observations', ln=True, align='C')
    pdf.set_font("Arial", size=8)
    headers = ['OBSERVEDATE', 'OBSERVATION', 'Category', 'Value', 'Type']
    result = df.group_by("OBSERVEDATE").agg([
    pl.col("OBSERVATION").first(),
    pl.col("CATEGORY").first().alias("Category"),
    pl.col("VALUE").first().alias("Value"),
    pl.col("TYPE").first().alias("Type"),
    ])
    data = result.sort('OBSERVEDATE').to_pandas().to_dict(orient="records")

    if not data[0][headers[0]]:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(40, 10, "No Observations",border=0, ln=True, align="C")
        pdf.set_font('Arial', '', 10)
    else:
        pdf.create_dynamic_table(data)

    
    pdf.output(filename)

# Route to handle AJAX call
@pdf_bp.route('/perform_task', methods=['POST'])
def perform_task():
    try:
        data = request.get_json()
        user_input = data.get('input')
        
        results = get_report_data(user_input)
        generate_pdf(results)

        if data:
            # Perform your task
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="No matching user found.")

    except Exception as e:
        return jsonify(success=False, error=str(e))