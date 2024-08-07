from flask import Blueprint # type: ignore

bp = Blueprint('views', __name__)

from . import auth, admin, staff, student
