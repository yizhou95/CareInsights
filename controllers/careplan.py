from flask import Blueprint, request, jsonify
from models import db
from models.careplan import CarePlans
from ulid import ULID

careplans_bp = Blueprint('careplans', __name__)

@careplans_bp.route('/', methods=['GET'])
def get_careplans():
    careplans = CarePlans.query.limit(500).all()
    return jsonify({"success": True, "careplans": [careplan.to_dict() for careplan in careplans]})

@careplans_bp.route('/', methods=['POST'])
def create_careplan():
    data = request.get_json()
    new_careplan = CarePlans(Id=str(ULID()), **data)
    db.session.add(new_careplan)
    db.session.commit()
    return jsonify({"success": True, "careplan": new_careplan.to_dict()}), 201

@careplans_bp.route('/<id>', methods=['GET'])
def get_careplan_by_id(id):
    careplan = CarePlans.query.get_or_404(id)
    return jsonify({"success": True, "careplan": careplan.to_dict()})

@careplans_bp.route('/patient/<patient_id>', methods=['GET'])
def get_careplans_by_patient_id(patient_id):
    careplans = CarePlans.query.filter_by(PATIENT=patient_id).all()
    return jsonify({"success": True, "careplans": [careplan.to_dict() for careplan in careplans]})

@careplans_bp.route('/<id>', methods=['PATCH'])
def update_careplan(id):
    data = request.get_json()
    careplan = CarePlans.query.get_or_404(id)
    for key, value in data.items():
        setattr(careplan, key, value)
    db.session.commit()
    return jsonify({"success": True, "careplan": careplan.to_dict()})

@careplans_bp.route('/<id>', methods=['DELETE'])
def delete_careplan(id):
    careplan = CarePlans.query.get_or_404(id)
    db.session.delete(careplan)
    db.session.commit()
    return jsonify({"success": True, "careplan": careplan.to_dict()})
