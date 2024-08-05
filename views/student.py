from datetime import datetime
from flask import Blueprint, request, jsonify, url_for
from models import Content, Comment, Subscription, Wishlist, Like
from app import db
from schemas import ContentSchema, CommentSchema, SubscriptionSchema, WishlistSchema, LikeSchema

bp = Blueprint('student', __name__, url_prefix='/students')

@bp.route('/content', methods=['GET'])
def list_all_content():
    content = Content.query.all()
    return ContentSchema(many=True).jsonify(content)

@bp.route('/content/<int:content_id>', methods=['GET'])
def view_specific_content(content_id):
    content = Content.query.get_or_404(content_id)
    return ContentSchema().jsonify(content)

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

@bp.route('/comments/<int:comment_id>', methods=['PATCH'])
def edit_own_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    if 'text' in data:
        comment.text = data['text']
    db.session.commit()
    return CommentSchema().jsonify(comment)

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def remove_own_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204

@bp.route('/subscriptions', methods=['POST'])
def subscribe_to_category():
    data = request.get_json()
    new_subscription = Subscription(
        user_id=data['user_id'],
        category_id=data['category_id'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_subscription)
    db.session.commit()
    return SubscriptionSchema().jsonify(new_subscription)

@bp.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def unsubscribe_from_category(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()
    return '', 204

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

@bp.route('/likes', methods=['POST'])
def like_or_dislike():
    data = request.get_json()
    new_like = Like(
        user_id=data['user_id'],
        content_id=data.get('content_id'),
        comment_id=data.get('comment_id'),
        type=data['type'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_like)
    db.session.commit()
    return LikeSchema().jsonify(new_like)


@bp.route('/share', methods=['POST'])
def share_content():
    try:
        # Extract data from the request
        data = request.json
        platform = data.get('platform')  # This might be used for further logic if needed
        content_id = data.get('content_id')

        # Check if content_id is provided
        if not content_id:
            return jsonify({"error": "content_id is required"}), 400

        # Generate a URL for sharing
        # Here, we are assuming you have an endpoint that displays content details
        shareable_url = url_for('content_details', content_id=content_id, _external=True)

        # Return the shareable URL
        return jsonify({"message": "Content shareable URL generated successfully", "url": shareable_url}), 200

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500