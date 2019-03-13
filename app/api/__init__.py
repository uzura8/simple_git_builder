from flask import Blueprint
from app.common.helper import url_static

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.context_processor
def helper_processor():
    return dict(url_static=url_static)

from . import routes
