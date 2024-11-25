from flask import Blueprint, request, jsonify
from models import db
from models.patient import Patients
from ulid import ULID

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/', methods=['POST'])
def create_patient():
    data = request.get_json()
    new_patient = Patients(Id=str(ULID()), **data)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created successfully!"}), 201

@patient_bp.route('/', methods=['GET'])
def get_patients():
    patients = Patients.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@patient_bp.route('/<id>', methods=['GET'])
def get_patient_by_id(id):
    patient = Patients.query.get_or_404(id)
    return jsonify(patient.to_dict())

@patient_bp.route('/<id>', methods=['PATCH'])
def update_patient(id):
    data = request.get_json()
    patient  = Patients.query.get_or_404(id)
    for key, value in data.items():
        setattr(patient , key, value)
    db.session.commit()
    return jsonify({"message": "Patient updated successfully!"})

@patient_bp.route('/<id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patients.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully!"})
