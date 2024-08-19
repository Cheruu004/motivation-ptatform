import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://moringa_platform_db_user:dEnyThz25UOcyxJpIEhv93E43KyNprBR@dpg-cr1d5frtq21c73crjt4g-a.oregon-postgres.render.com/moringa_platform_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    