
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # Create Flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Allow all origins for simplicity (not recommended for production)

    # Initialize Swagger
    swagger = Swagger(app, template_file='swagger/swagger.yaml')

    # Import and register blueprints
    from views import auth, admin, staff, student

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(staff.bp, url_prefix='/staff')
    app.register_blueprint(student.bp, url_prefix='/students')

    # Import models here to ensure they are registered with SQLAlchemy
    from models import User, Profile, Category, Content, Comment, Like, Subscription, Wishlist

    # Create database tables
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
