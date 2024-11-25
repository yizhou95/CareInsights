from flask import Blueprint, request, jsonify
from models import db
from models.immunization import Immunizations

immunization_bp = Blueprint('immunizations', __name__)

@immunization_bp.route('/', methods=['GET'])
def get_immunizations():
    immunizations = Immunizations.query.limit(500).all()
    return jsonify({"status": 200, "data": {"immunizations": [immunization.to_dict() for immunization in immunizations]}, "message": "Immunizations retrieved successfully!"})

@immunization_bp.route('/', methods=['POST'])
def create_immunization():
    data = request.get_json()
    new_immunization = Immunizations(**data)
    db.session.add(new_immunization)
    db.session.commit()
    return jsonify({"status": 200, "data": {"immunization": new_immunization.to_dict()}, "message": "Immunization saved in database successfully!"})

@immunization_bp.route('/<id>', methods=['GET'])
def get_immunization_by_id(id):
    immunization = Immunizations.query.filter_by(ID=id).first_or_404()
    return jsonify({"status": 200, "data": {"immunization": immunization.to_dict()}, "message": "Immunization retrieved successfully!"})

@immunization_bp.route('/patient/<patient_id>', methods=['GET'])
def get_immunizations_by_patient_id(patient_id):
    immunizations = Immunizations.query.filter_by(PATIENT=patient_id).all()
    return jsonify({"status": 200, "data": {"immunizations": [immunization.to_dict() for immunization in immunizations]}, "message": "Immunizations retrieved successfully!"})

@immunization_bp.route('/<id>', methods=['PATCH'])
def update_immunization(id):
    data = request.get_json()
    immunization = Immunizations.query.filter_by(ID=id).first_or_404()
    for key, value in data.items():
        setattr(immunization, key, value)
    db.session.commit()
    return jsonify({"status": 200, "data": {"immunization": immunization.to_dict()}, "message": "Immunization updated successfully!"})

@immunization_bp.route('/<id>', methods=['DELETE'])
def delete_immunization(id):
    immunization = Immunizations.query.filter_by(ID=id).first_or_404()
    db.session.delete(immunization)
    db.session.commit()
    return jsonify({"status": 200, "data": {"immunization": immunization.to_dict()}, "message": "Immunization deleted successfully!"})
