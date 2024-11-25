from flask import Blueprint, request, jsonify
from models import db
from models.supplies import Supplies
from werkzeug.exceptions import BadRequest, NotFound

supplies_bp = Blueprint('supplies', __name__)

@supplies_bp.route('/', methods=['GET'])
def get_supplies():
    supplies = Supplies.query.limit(500).all()
    return jsonify({
        "status": 200,
        "data": {"supplies": [supply.to_dict() for supply in supplies]},
        "message": "Supplies retrieved successfully!"
    })

@supplies_bp.route('/', methods=['POST'])
def create_supplies():
    data = request.get_json()
    if not data:
        raise BadRequest("Invalid data provided for creating supplies.")

    supply = Supplies(**data)
    db.session.add(supply)
    db.session.commit()

    return jsonify({
        "status": 201,
        "data": {"supply": supply.to_dict()},
        "message": "Supplies created successfully!"
    })

@supplies_bp.route('/<id>', methods=['GET'])
def get_supplies_by_id(id):
    supply = Supplies.query.filter_by(ID=id).first()
    if not supply:
        raise NotFound("Supplies not found")
    return jsonify({
        "status": 200,
        "data": {"supply": supply.to_dict()},
        "message": "Supplies retrieved successfully!"
    })

@supplies_bp.route('/<id>', methods=['PATCH'])
def update_supplies(id):
    data = request.get_json()
    if not data:
        raise BadRequest("Invalid data provided for updating supplies.")

    supply = Supplies.query.filter_by(ID=id).first()
    if not supply:
        raise NotFound("Supplies not found")

    for key, value in data.items():
        setattr(supply, key, value)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"supply": supply.to_dict()},
        "message": "Supplies updated successfully!"
    })

@supplies_bp.route('/<id>', methods=['DELETE'])
def delete_supplies(id):
    supply = Supplies.query.filter_by(ID=id).first()
    if not supply:
        raise NotFound("Supplies not found")

    db.session.delete(supply)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"id": id},
        "message": "Supplies deleted successfully!"
    })
