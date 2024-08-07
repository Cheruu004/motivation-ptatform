from datetime import datetime
from flask import Blueprint, request, jsonify # type: ignore
from models import User, Profile, Content, Comment, Wishlist
from app import db
from schemas import ProfileSchema, ContentSchema, CommentSchema, WishlistSchema

bp = Blueprint('student', __name__, url_prefix='/students')

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

@bp.route('/content', methods=['GET'])
def list_all_content():
    content = Content.query.all()
    return ContentSchema(many=True).jsonify(content)

@bp.route('/content/<int:content_id>', methods=['GET'])
def view_specific_content(content_id):
    content = Content.query.get_or_404(content_id)
    return ContentSchema().jsonify(content)

@bp.route('/content', methods=['POST'])
def post_content():
    data = request.get_json()
    new_content = Content(
        title=data['title'],
        description=data.get('description', ''),
        content_type=data['content_type'],
        content_url=data['content_url'],
        category_id=data['category_id'],
        created_by=data['user_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_content)
    db.session.commit()
    return ContentSchema().jsonify(new_content)

@bp.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    new_comment = Comment(
        content_id=data['content_id'],
        user_id=data['user_id'],
        text=data['text'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()
    return CommentSchema().jsonify(new_comment)

@bp.route('/comments/<int:comment_id>/reply', methods=['POST'])
def reply_to_comment(comment_id):
    data = request.get_json()
    new_comment = Comment(
        content_id=data['content_id'],
        user_id=data['user_id'],
        text=data['text'],
        parent_comment_id=comment_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()
    return CommentSchema().jsonify(new_comment)

@bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    new_wishlist_item = Wishlist(
        user_id=data['user_id'],
        content_id=data['content_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_wishlist_item)
    db.session.commit()
    return WishlistSchema().jsonify(new_wishlist_item)

@bp.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
def remove_from_wishlist(wishlist_id):
    wishlist_item = Wishlist.query.get_or_404(wishlist_id)
    db.session.delete(wishlist_item)
    db.session.commit()
    return '', 204

@bp.route('/comments/<int:content_id>', methods=['GET'])
def list_comments(content_id):
    comments = Comment.query.filter_by(content_id=content_id).all()
    return CommentSchema(many=True).jsonify(comments)

@bp.route('/comments/replies/<int:comment_id>', methods=['GET'])
def list_replies(comment_id):
    replies = Comment.query.filter_by(parent_comment_id=comment_id).all()
    return CommentSchema(many=True).jsonify(replies)
