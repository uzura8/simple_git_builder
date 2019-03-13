from flask import render_template
from . import bp


@bp.before_request
def before_request():
    pass


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
