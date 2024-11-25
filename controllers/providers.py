from flask import Blueprint, request, jsonify
from models import db
from models.provider import Providers
from werkzeug.exceptions import NotFound

provider_bp = Blueprint('providers', __name__)

@provider_bp.route('/', methods=['GET'])
def get_all_providers():
    providers = Providers.query.limit(1000).all()
    return jsonify({
        "status": 200,
        "data": {"providers": [provider.to_dict() for provider in providers]},
        "message": "Providers retrieved successfully!"
    })

@provider_bp.route('/<id>', methods=['GET'])
def get_provider_by_id(id):
    provider = Providers.query.filter_by(Id=id).first()
    if not provider:
        raise NotFound("Provider not found")
    return jsonify({
        "status": 200,
        "data": {"provider": provider.to_dict()},
        "message": "Provider retrieved successfully!"
    })

@provider_bp.route('/', methods=['POST'])
def create_provider():
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while creating provider."}), 404

    provider = Providers(Id=generate_id(), **data)  # Assuming generate_id() generates a unique ID
    db.session.add(provider)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"provider": provider.to_dict()},
        "message": "Provider created successfully!"
    })

@provider_bp.route('/<id>', methods=['PATCH'])
def update_provider(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while updating provider."}), 404

    provider = Providers.query.filter_by(Id=id).first()
    if not provider:
        raise NotFound("Provider not found")

    for key, value in data.items():
        setattr(provider, key, value)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"provider": provider.to_dict()},
        "message": "Provider updated successfully!"
    })

@provider_bp.route('/<id>', methods=['DELETE'])
def delete_provider(id):
    provider = Providers.query.filter_by(Id=id).first()
    if not provider:
        raise NotFound("Provider not found")

    db.session.delete(provider)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"id": id},
        "message": "Provider deleted successfully!"
    })

def generate_id():
    # Placeholder for ULID or any custom ID generator logic
    import ulid
    return str(ulid.ulid())
