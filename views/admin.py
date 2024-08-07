from datetime import datetime
from flask import Blueprint, request, jsonify # type: ignore
from models import User, Content, Category
from app import db
from schemas import UserSchema, ContentSchema, CategorySchema

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    # Ensure the required fields are present
    if not all(key in data for key in ('username', 'email', 'password_hash', 'role')):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create a new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash'],
        role=data['role']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added successfully"}), 201
@bp.route('/users/<int:user_id>/deactivate', methods=['PATCH'])
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.active = False
    db.session.commit()
    return UserSchema().jsonify(user)

@bp.route('/content/<int:content_id>/approve', methods=['PATCH'])
def approve_content(content_id):
    content = Content.query.get_or_404(content_id)
    content.approved_by = request.json['approved_by']
    db.session.commit()
    return ContentSchema().jsonify(content)

@bp.route('/content/<int:content_id>', methods=['DELETE'])
def remove_flagged_content(content_id):
    content = Content.query.get(content_id)
    if content is None:
        return jsonify({"error": "Content not found"}), 404
    
    db.session.delete(content)
    db.session.commit()
    return '', 204

@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(
        name=data['name'],
        description=data['description'],
        created_by=data['created_by'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_category)
    db.session.commit()
    return CategorySchema().jsonify(new_category)
