from app import db
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey,Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

user_category_association = Table(
    'user_category', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True),
    Column('subscribed_at', db.DateTime, default=datetime.utcnow)
)

class ActionType(PyEnum):
    like = "like"  # Adjusted to match PostgreSQL enum values
    dislike = "dislike"  # Adjusted to match PostgreSQL enum values

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)  # 'admin', 'student', 'staff'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    subscribed_categories = relationship('Category', secondary=user_category_association, back_populates='subscribers')
    likes_dislikes = relationship('LikeDislike', back_populates='user')


    def subscribe_to_category(self, category):
        if category not in self.subscribed_categories:
            self.subscribed_categories.append(category)
            db.session.commit()

    def unsubscribe_from_category(self, category):
        if category in self.subscribed_categories:
            self.subscribed_categories.remove(category)
            db.session.commit()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    subscribers = relationship('User', secondary=user_category_association, back_populates='subscribed_categories')


class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(64), nullable=False)  # 'video', 'audio', 'article'
    content_url = db.Column(db.String(256), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(256), nullable=True)  # New column for flag reason
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    likes_dislikes = relationship('LikeDislike', back_populates='content')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

class LikeDislike(db.Model):
    __tablename__ = 'like_dislike'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    type = db.Column(Enum(ActionType), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='likes_dislikes')
    content = relationship('Content', back_populates='likes_dislikes')