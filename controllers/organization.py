from flask import Blueprint, request, jsonify
from models import db
from models.organization import Organizations
import ulid

organization_bp = Blueprint('organizations', __name__)

@organization_bp.route('/', methods=['GET'])
def get_organizations():
    organizations = Organizations.query.all()
    return jsonify({
        "status": 200,
        "data": {"organizations": [organization.to_dict() for organization in organizations]},
        "message": "Organizations retrieved successfully!"
    })

@organization_bp.route('/', methods=['POST'])
def create_organization():
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while creating organization."}), 404

    data["Id"] = str(ulid.ulid())  # Generate ULID for the organization
    new_organization = Organizations(**data)
    db.session.add(new_organization)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"organization": new_organization.to_dict()},
        "message": "Organization created successfully!"
    })

@organization_bp.route('/<id>', methods=['GET'])
def get_organization_by_id(id):
    organization = Organizations.query.filter_by(Id=id).first()
    if not organization:
        return jsonify({"status": 404, "message": "Organization not found"}), 404

    return jsonify({
        "status": 200,
        "data": {"organization": organization.to_dict()},
        "message": "Organization retrieved successfully!"
    })

@organization_bp.route('/<id>', methods=['PATCH'])
def update_organization(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while updating organization."}), 404

    organization = Organizations.query.filter_by(Id=id).first()
    if not organization:
        return jsonify({"status": 404, "message": "Organization not found"}), 404

    for key, value in data.items():
        setattr(organization, key, value)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"organization": organization.to_dict()},
        "message": "Organization updated successfully!"
    })

@organization_bp.route('/<id>', methods=['DELETE'])
def delete_organization(id):
    organization = Organizations.query.filter_by(Id=id).first()
    if not organization:
        return jsonify({"status": 404, "message": "Organization not found"}), 404

    db.session.delete(organization)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"id": id},
        "message": "Organization deleted successfully!"
    })
