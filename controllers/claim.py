from flask import Blueprint, request, jsonify
from models import db
from models.claim import ClaimsTransactions
from ulid import ULID
from datetime import datetime

claims_bp = Blueprint('claims', __name__)

@claims_bp.route('/', methods=['GET'])
def get_claims():
    claims = ClaimsTransactions.query.filter(ClaimsTransactions.FROMDATE >= datetime(2007, 1, 1)).limit(500).all()
    return jsonify({"status": 200, "data": {"claims": [claim.to_dict() for claim in claims]}, "message": "Claims retrieved successfully!"})

@claims_bp.route('/', methods=['POST'])
def create_claim():
    data = request.get_json()
    new_claim = ClaimsTransactions(ID=str(ULID()), **data)
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({"status": 200, "data": {"claim": new_claim.to_dict()}, "message": "Claim created successfully!"})

@claims_bp.route('/<id>', methods=['GET'])
def get_claim_by_id(id):
    claim = ClaimsTransactions.query.get_or_404(id)
    return jsonify({"status": 200, "data": {"claim": claim.to_dict()}, "message": "Claim retrieved successfully!"})

@claims_bp.route('/patient/<patient_id>', methods=['GET'])
def get_claims_by_patient_id(patient_id):
    claims = ClaimsTransactions.query.filter_by(PATIENTID=patient_id).limit(100).all()
    return jsonify({"status": 200, "data": {"claims": [claim.to_dict() for claim in claims]}, "message": "Claims retrieved successfully!"})

@claims_bp.route('/<id>', methods=['PATCH'])
def update_claim(id):
    data = request.get_json()
    claim = ClaimsTransactions.query.get_or_404(id)
    for key, value in data.items():
        setattr(claim, key, value)
    db.session.commit()
    return jsonify({"status": 200, "data": {"claim": claim.to_dict()}, "message": "Claim updated successfully!"})

@claims_bp.route('/<id>', methods=['DELETE'])
def delete_claim(id):
    claim = ClaimsTransactions.query.get_or_404(id)
    db.session.delete(claim)
    db.session.commit()
    return jsonify({"status": 200, "data": {"claim": claim.to_dict()}, "message": "Claim deleted successfully!"})
