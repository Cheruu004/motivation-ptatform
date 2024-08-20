from datetime import datetime
from flask import Blueprint, request, jsonify # type: ignore
from models import User, Content, Category
from app import db
from schemas import UserSchema, ContentSchema, CategorySchema
from flask_cors import CORS
from flask import Flask, jsonify

bp = Blueprint('admin', __name__, url_prefix='/admin')
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

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

@bp.route('/content', methods=['POST'])
def post_content():
    data = request.get_json()
    new_content = Content(
        title=data['title'],
        description=data['description'],
        content_type=data['content_type'],
        content_url=data['content_url'],
        category_id=data['category_id'],
        created_by=data['created_by'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_content)
    db.session.commit()
    return ContentSchema().jsonify(new_content)

@bp.route('/content/<int:content_id>/approve', methods=['PATCH'])
def approve_content(content_id):
    content = Content.query.get_or_404(content_id)
    data = request.get_json()
    content.approved_by = data.get('approved_by')
    db.session.commit()
    return ContentSchema().jsonify(content)

@bp.route('/content/<int:content_id>/flag', methods=['PATCH'])
def flag_content(content_id):
    data = request.get_json()
    reason = data.get('reason')    
    content = Content.query.get_or_404(content_id)
    
    if content.flagged:
        return jsonify({"message": "Content is already flagged."}), 400
    
    content.flagged = True
    content.flag_reason = reason
    content.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({"message": "Content flagged successfully."}), 200

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
    
    if not data or 'created_by' not in data:
        return jsonify({"error": "'created_by' field is required"}), 400
    
    new_category = Category(
        name=data.get('name', ''),
        description=data.get('description', ''),
        created_by=data['created_by'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.session.add(new_category)
    db.session.commit()
    
    return CategorySchema().jsonify(new_category)


@bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return UserSchema(many=True).jsonify(users)

@bp.route('/content', methods=['GET'])
def get_content():
    content = Content.query.all()
    return ContentSchema(many=True).jsonify(content)

@bp.route('/analytics', methods=['GET'])
def get_analytics():
    total_users = User.query.count()
    total_staff = User.query.filter_by(role='staff').count()
    total_students = User.query.filter_by(role='student').count()
    total_content = Content.query.count()
    
    return jsonify({
        "totalUsers": total_users,
        "totalStaff": total_staff,
        "totalStudents": total_students,
        "totalContent": total_content
    })

@bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return CategorySchema(many=True).jsonify(categories)