from datetime import datetime
from flask import Blueprint, request, jsonify
from models import User, Profile, Content, Comment, Wishlist, Category
from app import db
from schemas import ProfileSchema, ContentSchema, CommentSchema, WishlistSchema, CategorySchema

bp = Blueprint('student', __name__, url_prefix='/students')

# Create a new profile
@bp.route('/profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash'],
        role='student',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    new_profile = Profile(
        user_id=new_user.id,
        bio=data.get('bio', ''),
        profile_picture_url=data.get('profile_picture_url', ''),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_profile)
    db.session.commit()
    return ProfileSchema().jsonify(new_profile)

# Get a profile by user ID
@bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile is None:
        return jsonify({"error": "Profile not found"}), 404
    return ProfileSchema().jsonify(profile)

# Update a profile
@bp.route('/profile/<int:user_id>', methods=['PATCH'])
def update_profile(user_id):
    data = request.get_json()
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile is None:
        return jsonify({"error": "Profile not found"}), 404
    
    profile.bio = data.get('bio', profile.bio)
    profile.profile_picture_url = data.get('profile_picture_url', profile.profile_picture_url)
    profile.updated_at = datetime.utcnow()
    
    db.session.commit()
    return ProfileSchema().jsonify(profile)

# Delete a profile
@bp.route('/profile/<int:user_id>', methods=['DELETE'])
def delete_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile is None:
        return jsonify({"error": "Profile not found"}), 404
    
    db.session.delete(profile)
    db.session.commit()
    return '', 204

# List all content
@bp.route('/content', methods=['GET'])
def list_all_content():
    content = Content.query.all()
    return ContentSchema(many=True).jsonify(content)

# View specific content
@bp.route('/content/<int:content_id>', methods=['GET'])
def view_specific_content(content_id):
    content = Content.query.get_or_404(content_id)
    return ContentSchema().jsonify(content)

# Post new content
@bp.route('/content', methods=['POST'])
def post_content():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if not data.get('title') or not data.get('content_url') or not data.get('content_type'):
        return jsonify({"error": "Title, content URL, and content type are required"}), 400

    new_content = Content(
        title=data['title'],
        description=data.get('description', ''),
        content_type=data['content_type'],
        content_url=data['content_url'],
        category_id=data.get('category_id'),
        created_by=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_content)
    db.session.commit()
    return ContentSchema().jsonify(new_content)

# Comment on a post
@bp.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    new_comment = Comment(
        content_id=data['content_id'],
        user_id=user_id,
        text=data['text'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()
    return CommentSchema().jsonify(new_comment)

# Reply to a comment
@bp.route('/comments/<int:comment_id>/reply', methods=['POST'])
def reply_to_comment(comment_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    new_comment = Comment(
        content_id=data['content_id'],
        user_id=user_id,
        text=data['text'],
        parent_comment_id=comment_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()
    return CommentSchema().jsonify(new_comment)

# List comments for a specific content
@bp.route('/comments/<int:content_id>', methods=['GET'])
def list_comments(content_id):
    comments = Comment.query.filter_by(content_id=content_id).all()
    return CommentSchema(many=True).jsonify(comments)

# List replies to a specific comment
@bp.route('/comments/replies/<int:comment_id>', methods=['GET'])
def list_replies(comment_id):
    replies = Comment.query.filter_by(parent_comment_id=comment_id).all()
    return CommentSchema(many=True).jsonify(replies)

# Add to wishlist
@bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    new_wishlist_item = Wishlist(
        user_id=user_id,
        content_id=data['content_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_wishlist_item)
    db.session.commit()
    return WishlistSchema().jsonify(new_wishlist_item)

# Remove from wishlist
@bp.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
def remove_from_wishlist(wishlist_id):
    wishlist_item = Wishlist.query.get_or_404(wishlist_id)
    db.session.delete(wishlist_item)
    db.session.commit()
    return '', 204

# List all wishlist items for a user
@bp.route('/wishlist/user/<int:user_id>', methods=['GET'])
def list_user_wishlist(user_id):
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    return WishlistSchema(many=True).jsonify(wishlist_items)

# List all categories
@bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return CategorySchema(many=True).jsonify(categories)

@bp.route('/categories/subscribe', methods=['POST'])
def subscribe_to_category():
    data = request.get_json()
    user_id = data.get('user_id')
    category_id = data.get('category_id')

    if not user_id or not category_id:
        return jsonify({"error": "User ID and Category ID are required"}), 400

    user = User.query.get(user_id)
    category = Category.query.get(category_id)

    if not user or not category:
        return jsonify({"error": "User or Category not found"}), 404

    if category in user.subscribed_categories:
        return jsonify({"error": "Already subscribed to this category"}), 400

    user.subscribe_to_category(category)
    return jsonify({"message": "Successfully subscribed to category"}), 200

@bp.route('/categories/unsubscribe', methods=['POST'])
def unsubscribe_from_category():
    data = request.get_json()
    user_id = data.get('user_id')
    category_id = data.get('category_id')

    if not user_id or not category_id:
        return jsonify({"error": "User ID and Category ID are required"}), 400

    user = User.query.get(user_id)
    category = Category.query.get(category_id)

    if not user or not category:
        return jsonify({"error": "User or Category not found"}), 404

    if category not in user.subscribed_categories:
        return jsonify({"error": "Not subscribed to this category"}), 404

    user.unsubscribe_from_category(category)
    return jsonify({"message": "Successfully unsubscribed from category"}), 200

@bp.route('/comments/count/<int:content_id>', methods=['GET'])
def get_comment_count(content_id):
    count = Comment.query.filter_by(content_id=content_id).count()
    return jsonify({'count': count})