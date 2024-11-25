from flask import Blueprint, request, jsonify
from models import db
from models.encounter import Encounters
from ulid import ULID

encounter_bp = Blueprint('encounters', __name__)

@encounter_bp.route('/', methods=['GET'])
def get_encounters():
    encounters = Encounters.query.limit(500).all()
    return jsonify({"status": 200, "data": {"encounters": [encounter.to_dict() for encounter in encounters]}, "message": "Encounters retrieved successfully!"})

@encounter_bp.route('/', methods=['POST'])
def create_encounter():
    data = request.get_json()
    new_encounter = Encounters(Id=ULID(), **data)
    db.session.add(new_encounter)
    db.session.commit()
    return jsonify({"status": 200, "data": {"encounter": new_encounter.to_dict()}, "message": "Encounter saved in database successfully!"})

@encounter_bp.route('/<id>', methods=['GET'])
def get_encounter_by_id(id):
    encounter = Encounters.query.filter_by(Id=id).first_or_404()
    return jsonify({"status": 200, "data": {"encounter": encounter.to_dict()}, "message": "Encounter retrieved successfully!"})

@encounter_bp.route('/patient/<patient_id>', methods=['GET'])
def get_encounters_by_patient_id(patient_id):
    encounters = Encounters.query.filter_by(PATIENT=patient_id).all()
    return jsonify({"status": 200, "data": {"encounters": [encounter.to_dict() for encounter in encounters]}, "message": "Encounters retrieved successfully!"})

@encounter_bp.route('/<id>', methods=['PATCH'])
def update_encounter(id):
    data = request.get_json()
    encounter = Encounters.query.filter_by(Id=id).first_or_404()
    for key, value in data.items():
        setattr(encounter, key, value)
    db.session.commit()
    return jsonify({"status": 200, "data": {"encounter": encounter.to_dict()}, "message": "Encounter updated successfully!"})

@encounter_bp.route('/<id>', methods=['DELETE'])
def delete_encounter(id):
    encounter = Encounters.query.filter_by(Id=id).first_or_404()
    db.session.delete(encounter)
    db.session.commit()
    return jsonify({"status": 200, "data": {"encounter": encounter.to_dict()}, "message": "Encounter deleted successfully!"})
