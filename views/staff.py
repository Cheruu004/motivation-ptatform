# from datetime import datetime
# from flask import Blueprint, request, jsonify # type: ignore
# from models import Content, Comment
# from app import db
# from schemas import ContentSchema, CommentSchema

# bp = Blueprint('staff', __name__, url_prefix='/staff')

# @bp.route('/content', methods=['POST'])
# def post_content():
#     data = request.get_json()
#     new_content = Content(
#         title=data['title'],
#         description=data['description'],
#         content_type=data['content_type'],
#         content_url=data['content_url'],
#         category_id=data['category_id'],
#         created_by=data['created_by'],
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow()
#     )
#     db.session.add(new_content)
#     db.session.commit()
#     return ContentSchema().jsonify(new_content)

# @bp.route('/content/<int:content_id>', methods=['PATCH'])
# def edit_content(content_id):
#     content = Content.query.get_or_404(content_id)
#     data = request.get_json()
#     if 'title' in data:
#         content.title = data['title']
#     if 'description' in data:
#         content.description = data['description']
#     if 'content_type' in data:
#         content.content_type = data['content_type']
#     if 'content_url' in data:
#         content.content_url = data['content_url']
#     db.session.commit()
#     return ContentSchema().jsonify(content)

# @bp.route('/content/<int:content_id>', methods=['DELETE'])
# def remove_own_content(content_id):
#     content = Content.query.get_or_404(content_id)
#     db.session.delete(content)
#     db.session.commit()
#     return '', 204

# @bp.route('/content/<int:content_id>/approve', methods=['PATCH'])
# def approve_content(content_id):
#     content = Content.query.get_or_404(content_id)
#     content.approved_by = request.json['approved_by']
#     db.session.commit()
#     return ContentSchema().jsonify(content)

# @bp.route('/content/<int:content_id>/flag', methods=['PATCH'])
# def flag_content(content_id):
#     content = Content.query.get_or_404(content_id)
#     content.flagged = True
#     db.session.commit()
#     return ContentSchema().jsonify(content)

# @bp.route('/comments', methods=['POST'])
# def post_comment():
#     data = request.get_json()
#     new_comment = Comment(
#         content_id=data['content_id'],
#         user_id=data['user_id'],
#         text=data['text'],
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow()
#     )
#     db.session.add(new_comment)
#     db.session.commit()
#     return CommentSchema().jsonify(new_comment)

# @bp.route('/comments/<int:comment_id>/reply', methods=['POST'])
# def reply_to_comment(comment_id):
#     data = request.get_json()
#     new_comment = Comment(
#         content_id=data['content_id'],
#         user_id=data['user_id'],
#         text=data['text'],
#         parent_comment_id=comment_id,
#         created_at=datetime.utcnow(),
#         updated_at=datetime.utcnow()
#     )
#     db.session.add(new_comment)
#     db.session.commit()
#     return CommentSchema().jsonify(new_comment)

# @bp.route('/comments/<int:comment_id>', methods=['PATCH'])
# def edit_own_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     data = request.get_json()
#     if 'text' in data:
#         comment.text = data['text']
#     db.session.commit()
#     return CommentSchema().jsonify(comment)

# @bp.route('/comments/<int:comment_id>', methods=['DELETE'])
# def remove_own_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     db.session.delete(comment)
#     db.session.commit()
#     return '', 204


from datetime import datetime
from flask import Blueprint, request, jsonify
from models import Content, Comment
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
def remove_own_content(content_id):
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    return '', 200

@bp.route('/content/<int:content_id>/approve', methods=['PATCH'])
def approve_content(content_id):
    content = Content.query.get_or_404(content_id)
    content.approved_by = request.json['approved_by']
    db.session.commit()
    return ContentSchema().jsonify(content)

@bp.route('/content/<int:content_id>/flag', methods=['PATCH'])
def flag_content(content_id):
    content = Content.query.get_or_404(content_id)
    content.flagged = True
    db.session.commit()
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
