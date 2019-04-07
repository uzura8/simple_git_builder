import re
import calendar
import datetime
from flask import jsonify, request
from . import bp
from app import db, InvalidArgumentException
from app.models import Account, Transaction, Category
from app.common.date import validate_date


@bp.before_request
def before_request():
    pass


@bp.route('/transactions', methods=['GET'])
def transactions():
    year, month = validate_month(request.args.get('month'))
    _, lastday = calendar.monthrange(year, month)
    items = []
    items = Transaction.query.outerjoin(
        Account,
        Transaction.account_code == Account.code
    ).filter(db.and_(
        Transaction.date >= datetime.date(year, month, 1),
        Transaction.date <= datetime.date(year, month, lastday),
    )).order_by(Transaction.date.desc()).all()
    body = [item.to_dict() for item in items]
    return jsonify(body), 200


@bp.route('/transactions/<int:trans_id>', methods=['POST'])
def update_transaction_category(trans_id=0, cate_id=0):
    if not trans_id:
        raise InvalidArgumentException
    trans = Transaction.get_one_by_id(trans_id)
    if not trans:
        raise InvalidArgumentException

    is_updated = False

    date = request.form.get('date', type=str, default=None)
    if date is not None:
        if not validate_date(date):
            raise InvalidArgumentException
        trans.date = date
        is_updated = True

    name = request.form.get('name', type=str, default=None)
    if name is not None:
        if not name or len(name) > 512:
            raise InvalidArgumentException
        trans.name = name
        is_updated = True

    amount = request.form.get('amount', type=int, default=None)
    if amount is not None:
        trans.amount = amount
        is_updated = True

    cate_id = request.form.get('category_id', type=int)
    if cate_id:
        cate = Category.get_one_by_id(cate_id)
        if not cate:
            raise InvalidArgumentException
        trans.category_id = cate_id
        is_updated = True

    is_disabled = request.form.get('is_disabled', type=int, default=None)
    if is_disabled is not None:
        if is_disabled not in [0, 1]:
            raise InvalidArgumentException
        trans.is_disabled = is_disabled
        is_updated = True

    if is_updated:
        db.session.commit()

    return 'OK', 200


@bp.route('/categories', methods=['GET'])
def categories():
    categories = Category.get_categories(is_json=True)
    return jsonify(categories), 200


def validate_month(month_str):
    if not month_str:
        raise InvalidArgumentException
    m = re.search(r'([0-9]{4})\-([0-9]{2})', month_str)
    if not m:
        raise InvalidArgumentException
    year = int(m.group(1))
    month = int(m.group(2))
    if month < 1 or month > 12:
        raise InvalidArgumentException
    return year, month
