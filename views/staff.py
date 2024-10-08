

from datetime import datetime
from flask import Blueprint, abort, request, jsonify
from models import Content, Comment, LikeDislike, ActionType,User
from app import db
from schemas import ContentSchema, CommentSchema

bp = Blueprint('staff', __name__, url_prefix='/staff')

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


@bp.route('/content/<int:content_id>', methods=['PATCH'])
def edit_content(content_id):
    content = Content.query.get_or_404(content_id)
    data = request.get_json()
    if 'title' in data:
        content.title = data['title']
    if 'description' in data:
        content.description = data['description']
    if 'content_type' in data:
        content.content_type = data['content_type']
    if 'content_url' in data:
        content.content_url = data['content_url']
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

@bp.route('/content/<int:content_id>/approve', methods=['PATCH'])
def approve_content(content_id):
    content = Content.query.get_or_404(content_id)
    content.approved_by = request.json['approved_by']
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

@bp.route('/content', methods=['GET'])
def get_content():
    content = Content.query.all()
    return ContentSchema(many=True).jsonify(content)

@bp.route('/comments', methods=['GET'])
def get_all_comments():
    comments = Comment.query.all()
    return CommentSchema(many=True).jsonify(comments)

@bp.route('/content/<int:content_id>/like_dislike', methods=['POST'])
def like_dislike_content(content_id):
    user_id = request.json.get('user_id')
    if not user_id:
        abort(401, description="User ID is required")

    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    content = Content.query.get(content_id)
    if not content:
        abort(404, description="Content not found")

    action_type_str = request.json.get('action_type')
    try:
        action_type = ActionType[action_type_str.lower()]  # Convert to lowercase to match enum values
    except KeyError:
        abort(400, description="Invalid action type")

    existing_action = LikeDislike.query.filter_by(user_id=user.id, content_id=content_id).first()
    
    if existing_action:
        if existing_action.type == action_type:
            db.session.delete(existing_action)
            db.session.commit()
            return jsonify({"message": "Removed action"}), 200
        else:
            existing_action.type = action_type
            db.session.commit()
            return jsonify({"message": "Updated action"}), 200
    else:
        new_action = LikeDislike(user_id=user.id, content_id=content_id, type=action_type)
        db.session.add(new_action)
        db.session.commit()
        return jsonify({"message": "Added action"}), 201

