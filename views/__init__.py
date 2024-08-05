from flask import Blueprint

bp = Blueprint('views', __name__)

from . import auth, admin, staff, student
