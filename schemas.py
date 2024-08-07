from app import ma
from models import User, Profile, Category, Content, Comment, Wishlist

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

class ContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Content

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
