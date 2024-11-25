from flask import Blueprint, request, jsonify
from models import db
from models.condition import Conditions

condition_bp = Blueprint('conditions', __name__)

@condition_bp.route('/', methods=['GET'])
def get_conditions():
    conditions = Conditions.query.limit(500).all()
    return jsonify({"status": 200, "data": {"conditions": [condition.to_dict() for condition in conditions]}, "message": "Conditions Fetched Successfully!"})

@condition_bp.route('/', methods=['POST'])
def create_condition():
    data = request.get_json()
    new_condition = Conditions(ENCOUNTER=data['ENCOUNTER'], **data)
    db.session.add(new_condition)
    db.session.commit()
    return jsonify({"status": 200, "data": {"condition": new_condition.to_dict()}, "message": "Condition created successfully!"})

@condition_bp.route('/<id>', methods=['GET'])
def get_condition_by_id(id):
    condition = Conditions.query.filter_by(ENCOUNTER=id).first_or_404()
    return jsonify({"status": 200, "data": {"condition": condition.to_dict()}, "message": "Condition by ID"})

@condition_bp.route('/patient/<patient_id>', methods=['GET'])
def get_conditions_by_patient_id(patient_id):
    conditions = Conditions.query.filter_by(PATIENT=patient_id).all()
    return jsonify({"status": 200, "data": {"conditions": [condition.to_dict() for condition in conditions]}, "message": "Condition by Patient ID"})

@condition_bp.route('/<id>', methods=['PATCH'])
def update_condition(id):
    data = request.get_json()
    condition = Conditions.query.filter_by(ENCOUNTER=id).first_or_404()
    for key, value in data.items():
        setattr(condition, key, value)
    db.session.commit()
    return jsonify({"status": 200, "data": {"condition": condition.to_dict()}, "message": "Condition updated"})

@condition_bp.route('/<id>', methods=['DELETE'])
def delete_condition(id):
    condition = Conditions.query.filter_by(ENCOUNTER=id).first_or_404()
    db.session.delete(condition)
    db.session.commit()
    return jsonify({"status": 200, "data": {"condition": condition.to_dict()}, "message": "Deleted Successfully!"})
