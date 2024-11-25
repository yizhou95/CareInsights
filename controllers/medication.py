from flask import Blueprint, request, jsonify
from models import db
from models.medication import Medications

medication_bp = Blueprint('medications', __name__)

@medication_bp.route('/', methods=['GET'])
def get_medications():
    medications = Medications.query.limit(500).all()
    return jsonify({"status": 200, "data": {"medications": [medication.to_dict() for medication in medications]}, "message": "Medications retrieved successfully!"})

@medication_bp.route('/', methods=['POST'])
def create_medication():
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while creating medication."}), 404
    
    new_medication = Medications(**data)
    db.session.add(new_medication)
    db.session.commit()
    return jsonify({"status": 200, "data": {"medication": new_medication.to_dict()}, "message": "Medication created successfully!"})

@medication_bp.route('/<id>', methods=['GET'])
def get_medication_by_id(id):
    medication = Medications.query.filter_by(ID=id).first()
    if not medication:
        return jsonify({"status": 404, "message": "Medication not found"}), 404
    return jsonify({"status": 200, "data": {"medication": medication.to_dict()}, "message": "Medication retrieved successfully!"})

@medication_bp.route('/patient/<patient_id>', methods=['GET'])
def get_medications_by_patient_id(patient_id):
    medications = Medications.query.filter_by(PATIENT=patient_id).all()
    if not medications:
        return jsonify({"status": 404, "message": "Medications not found"}), 404
    return jsonify({"status": 200, "data": {"medications": [medication.to_dict() for medication in medications]}, "message": "Medications retrieved successfully!"})

@medication_bp.route('/<id>', methods=['PATCH'])
def update_medication(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while updating medication."}), 404
    
    medication = Medications.query.filter_by(ID=id).first()
    if not medication:
        return jsonify({"status": 404, "message": "Medication not found"}), 404

    for key, value in data.items():
        setattr(medication, key, value)
    db.session.commit()
    return jsonify({"status": 200, "data": {"medication": medication.to_dict()}, "message": "Medication updated successfully!"})

@medication_bp.route('/<id>', methods=['DELETE'])
def delete_medication(id):
    medication = Medications.query.filter_by(ID=id).first()
    if not medication:
        return jsonify({"status": 404, "message": "Medication not found"}), 404
    
    db.session.delete(medication)
    db.session.commit()
    return jsonify({"status": 200, "data": {"medication": medication.to_dict()}, "message": "Medication deleted successfully!"})
