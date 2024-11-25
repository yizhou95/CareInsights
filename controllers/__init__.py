# Import the blueprints from the controllers
from .auth_controller import auth_bp
from .admin_controller import admin_bp
from .fhir_controller import fhir_bp
from .pdf_export_controller import pdf_bp
from .allergies import allergies_bp
from .careplan import careplans_bp
from .claim import claims_bp
from .condition import condition_bp
from .encounter import encounter_bp
from .immunizations import immunization_bp
from .medication import medication_bp
from .observation import observation_bp
from .organization import organization_bp
from .patient import patient_bp
from .procedures import procedure_bp
from .providers import provider_bp
from .supplies import supplies_bp

# Optionally, you could list them in an array for easy registration
all_blueprints = [
    (auth_bp, '/auth'),
    (admin_bp, '/admin'),
    (fhir_bp, '/api/fhir'),
    (pdf_bp, '/api/pdf'),
    (allergies_bp, '/api/allergies'),
    (careplans_bp, '/api/careplan'),
    (claims_bp, '/api/claim'),
    (condition_bp, '/api/condition'),
    (encounter_bp, '/api/encounter'),
    (immunization_bp, '/api/immunization'),
    (medication_bp, '/api/medication'),
    (observation_bp, '/api/observation'),
    (organization_bp, '/api/organization'),
    (patient_bp, '/api/patient'),
    (procedure_bp, '/api/procedure'),
    (provider_bp, '/api/provider'),
    (supplies_bp, '/api/supplies'),
]
