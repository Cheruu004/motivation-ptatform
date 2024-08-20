import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://moringa_platform_db_prod_user:iK9zHBfCMte6NKZU06kqfR1XRj2ZtEac@dpg-cr1phhtsvqrc73e1dhg0-a.oregon-postgres.render.com/moringa_platform_db_prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    