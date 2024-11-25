from flask import Blueprint, request, jsonify
from models import db
from models.observations import Observations

observation_bp = Blueprint('observations', __name__)

@observation_bp.route('/', methods=['GET'])
def get_observations():
    observation_type = request.args.get('type', default=None)

    observations = Observations.query.filter(
        Observations.CATEGORY.in_(['vital-signs', 'laboratory', 'survey'])
    ).limit(5500).all()

    if observation_type:
        observations = [obs for obs in observations if obs.CATEGORY == observation_type]

    return jsonify({
        "status": 200,
        "data": {"observations": [observation.to_dict() for observation in observations]},
        "message": "Observations retrieved successfully!"
    })

@observation_bp.route('/patient/<patient_id>', methods=['GET'])
def get_observations_by_patient_id(patient_id):
    observations = Observations.query.filter(
        Observations.CATEGORY.in_(['vital-signs']),
        Observations.PATIENT == patient_id,
        Observations.DESCRIPTION.in_(['Diastolic Blood Pressure', 'Systolic Blood Pressure', 'Heart Rate'])
    ).all()

    return jsonify({
        "status": 200,
        "data": {"observations": [observation.to_dict() for observation in observations]},
        "message": "Observations retrieved successfully!"
    })


@observation_bp.route('/', methods=['POST'])
def create_observation():
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while creating observation."}), 404
    
    new_observation = Observations(**data)
    db.session.add(new_observation)
    db.session.commit()
    
    return jsonify({
        "status": 200,
        "data": {"observation": new_observation.to_dict()},
        "message": "Observation created successfully!"
    })

@observation_bp.route('/<id>', methods=['GET'])
def get_observation_by_id(id):
    observation = Observations.query.filter_by(ID=id).first()
    if not observation:
        return jsonify({"status": 404, "message": "Observation not found"}), 404
    
    return jsonify({
        "status": 200,
        "data": {"observation": observation.to_dict()},
        "message": "Observation retrieved successfully!"
    })

@observation_bp.route('/<id>', methods=['PATCH'])
def update_observation(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 404, "message": "Something went wrong while updating observation."}), 404
    
    observation = Observations.query.filter_by(ID=id).first()
    if not observation:
        return jsonify({"status": 404, "message": "Observation not found"}), 404

    for key, value in data.items():
        setattr(observation, key, value)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"observation": observation.to_dict()},
        "message": "Observation updated successfully!"
    })

@observation_bp.route('/<id>', methods=['DELETE'])
def delete_observation(id):
    observation = Observations.query.filter_by(ID=id).first()
    if not observation:
        return jsonify({"status": 404, "message": "Observation not found"}), 404

    db.session.delete(observation)
    db.session.commit()

    return jsonify({
        "status": 200,
        "data": {"id": id},
        "message": "Observation deleted successfully!"
    })
