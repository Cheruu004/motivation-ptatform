import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://moringa_platform_db_prod_j4b0_user:McY1hkFt8rgpmYi56wlNPSO8MlH8N0G1@dpg-cr29qtbv2p9s738c99v0-a.oregon-postgres.render.com/moringa_platform_db_prod_j4b0')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    