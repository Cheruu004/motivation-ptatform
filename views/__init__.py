from flask import Blueprint # type: ignore

bp = Blueprint('views', __name__)

from . import auth, admin, staff, student


from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS configuration
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development

    # Register blueprints
    from .auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import bp as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .staff import bp as staff_blueprint
    app.register_blueprint(staff_blueprint, url_prefix='/staff')

    from .student import bp as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    return app
