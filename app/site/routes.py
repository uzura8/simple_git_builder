from flask import render_template
from . import bp


@bp.before_request
def before_request():
    pass


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


## For Let's encrypt confirmation
#@bp.route('/.well-known/acme-challenge/<filename>')
#def well_known(filename):
#    return render_template('.well-known/acme-challenge/'+ filename)
