from flask import Blueprint, request, jsonify
from models import db
from models.allergies import Allergies

allergies_bp = Blueprint('allergies', __name__)

@allergies_bp.route('/', methods=['POST'])
def create_allergy():
    data = request.get_json()
    new_allergy = Allergies(**data)
    db.session.add(new_allergy)
    db.session.commit()
    return jsonify({"message": "Allergy created successfully!"}), 201

@allergies_bp.route('/', methods=['GET'])
def get_all_allergies():
    allergies = Allergies.query.limit(500).all()
    return jsonify([allergy.to_dict() for allergy in allergies])

@allergies_bp.route('/<id>', methods=['GET'])
def get_allergy(id):
    allergy = Allergies.query.get_or_404(id)
    return jsonify(allergy.to_dict())

@allergies_bp.route('/patient/<patient_id>', methods=['GET'])
def get_allergies_by_patient_id(patient_id):
    allergies = Allergies.query.filter_by(PATIENT=patient_id).all()
    return jsonify([allergy.to_dict() for allergy in allergies])

@allergies_bp.route('/<id>', methods=['PATCH'])
def update_allergy(id):
    data = request.get_json()
    allergy = Allergies.query.get_or_404(id)
    for key, value in data.items():
        setattr(allergy, key, value)
    db.session.commit()
    return jsonify({"message": "Allergy updated successfully!"})

@allergies_bp.route('/<id>', methods=['DELETE'])
def delete_allergy(id):
    allergy = Allergies.query.get_or_404(id)
    db.session.delete(allergy)
    db.session.commit()
    return jsonify({"message": "Allergy deleted successfully!"})