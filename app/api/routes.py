from flask import jsonify, request
from . import bp
from app.models import Account, Transaction
#from app import db, InvalidArgumentException


@bp.before_request
def before_request():
    pass


@bp.route('/transactions', methods=['GET'])
def transactions():
    items = []
    items = Transaction.query.outerjoin(
        Account,
        Transaction.account_code == Account.code
    ).order_by(Transaction.date.desc()).all()
    body = [item.to_dict() for item in items]
    return jsonify(body), 200
