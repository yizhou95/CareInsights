from flask import Blueprint, request, jsonify
from models import db
from models.procedure import Procedures
from werkzeug.exceptions import NotFound

procedure_bp = Blueprint('procedures', __name__)

@procedure_bp.route('/', methods=['GET'])
def get_all_procedures():
    procedures = Procedures.query.limit(500).all()
    return jsonify({
        "status": 200,
        "data": {"procedures": [procedure.to_dict() for procedure in procedures]},
        "message": "Procedures retrieved successfully!"
    })

@procedure_bp.route('/<id>', methods=['GET'])
def get_procedure_by_id(id):
    procedure = Procedures.query.filter_by(ID=id).first()
    if not procedure:
        raise NotFound("Procedure not found")
    return jsonify({
        "status": 200,
        "data": {"procedure": procedure.to_dict()},
        "message": "Procedure retrieved successfully!"
    })

@procedure_bp.route('/', methods=['POST'])
def create_procedure():
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while creating procedure."}), 404
    
    procedure = Procedures(**data)
    db.session.add(procedure)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"procedure": procedure.to_dict()},
        "message": "Procedure created successfully!"
    })

@procedure_bp.route('/patient/<patient_id>', methods=['GET'])
def get_procedures_by_patient_id(patient_id):
    procedures = Procedures.query.filter_by(PATIENT=patient_id).all()
    if not procedures:
        raise NotFound("Procedures not found")

    return jsonify({
        "status": 200,
        "data": {"procedures": [procedure.to_dict() for procedure in procedures]},
        "message": "Procedures retrieved successfully!"
    })

@procedure_bp.route('/<id>', methods=['PATCH'])
def update_procedure(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while updating procedure."}), 404

    procedure = Procedures.query.filter_by(ID=id).first()
    if not procedure:
        raise NotFound("Procedure not found")

    for key, value in data.items():
        setattr(procedure, key, value)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"procedure": procedure.to_dict()},
        "message": "Procedure updated successfully!"
    })

@procedure_bp.route('/<id>', methods=['DELETE'])
def delete_procedure(id):
    procedure = Procedures.query.filter_by(ID=id).first()
    if not procedure:
        raise NotFound("Procedure not found")

    db.session.delete(procedure)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"id": id},
        "message": "Procedure deleted successfully!"
    })
