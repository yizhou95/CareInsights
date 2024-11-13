# Import the blueprints from the controllers
from .auth_controller import auth_bp
from .admin_controller import admin_bp

# Optionally, you could list them in an array for easy registration
all_blueprints = [
    (auth_bp, '/auth'),
    (admin_bp, '/admin')
]
