import re
import calendar
import datetime
import simplejson as json
from flask import jsonify, request
from . import bp, InvalidUsage
from app import db, InvalidArgumentException
from app.models import Account, Transaction, TransactionPreset, \
                       Category, Budget, Performance
from app.common.date import validate_date


@bp.before_request
def before_request():
    pass


@bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        values = {}
        date = request.form.get('date', type=str, default=None)
        if not date or not validate_date(date):
            raise InvalidUsage('Reauested param date is invalid')
        values['date'] = date

        name = request.form.get('name', type=str, default=None)
        if not name  or len(name) > 512:
            raise InvalidUsage('Reauested param name is invalid')
        values['name'] = name

        amount = int(request.form.get('amount', type=int, default=None))
        values['amount'] = amount

        cate_id = int(request.form.get('category_id', type=int))
        if cate_id:
            cate = Category.get_one_by_id(cate_id)
            if not cate:
                raise InvalidUsage('Reauested param category_id is invalid')
            values['category_id'] = cate_id
        else:
            raise InvalidUsage('Reauested param category_id is required')

        account_code = request.form.get('account_code', type=str, default=None)
        if account_code:
            account = Account.get_one_by_pk(account_code, 'code')
            if not account:
                raise InvalidUsage('Reauested param account_code is invalid')
            values['account_code'] = account_code
        else:
            values['account_code'] = 'manual'

        transaction = Transaction.create(values)
        if transaction is None:
            raise InvalidUsage('Database save error')

        body = transaction.to_dict()

    else:
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


@bp.route('/transactions/<int:trans_id>', methods=['POST', 'DELETE'])
def update_transaction_category(trans_id=0, cate_id=0):
    if not trans_id:
        raise InvalidUsage('Not Found', 404)
    trans = Transaction.get_one_by_id(trans_id)
    if not trans:
        raise InvalidUsage('Not Found', 404)

    if request.method == 'POST':
        is_updated = False

        date = request.form.get('date', type=str, default=None)
        if date is not None:
            if not validate_date(date):
                raise InvalidUsage('Reauested param date is invalid')
            trans.date = date
            is_updated = True

        name = request.form.get('name', type=str, default=None)
        if name is not None:
            if not name or len(name) > 512:
                raise InvalidUsage('Reauested param name is invalid')
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
                raise InvalidUsage('Reauested param category_id is invalid')
            trans.category_id = cate_id
            is_updated = True

        account_code = request.form.get('account_code', type=str, default=None)
        if account_code:
            account = Account.get_one_by_pk(account_code, 'code')
            if not account:
                raise InvalidUsage('account_code is invalid')
            trans.account_code = account_code

        is_disabled = request.form.get('is_disabled', type=int, default=None)
        if is_disabled is not None:
            if is_disabled not in [0, 1]:
                raise InvalidUsage('Reauested is_disabled date is invalid')
            trans.is_disabled = is_disabled
            is_updated = True

        if is_updated:
            db.session.commit()

        return jsonify(trans.to_dict()), 200

    elif request.method == 'DELETE':
        trans = Transaction.delete(trans_id)

        return jsonify(trans), 200


@bp.route('/presets', methods=['GET', 'POST'])
def transaction_presets():
    if request.method == 'POST':
        values = validate_presets(request.form, True)
        preset = TransactionPreset.save(values)
        if preset is None:
            raise InvalidUsage('Create preset error')
        body = preset.to_dict()

    else:
        items = TransactionPreset.query.all()
        body = [item.to_dict() for item in items]

    return jsonify(body), 200


@bp.route('/presets/<int:preset_id>', methods=['POST', 'DELETE'])
def update_transaction_preset(preset_id=0):
    if request.method == 'POST':
        values = validate_presets(request.form)
        preset = TransactionPreset.save(values, preset_id)
        if preset is None:
            raise InvalidUsage('Create preset error')

        return jsonify(preset.to_dict()), 200

    elif request.method == 'DELETE':
        preset = TransactionPreset.delete(preset_id)

        return jsonify(preset), 200


@bp.route('/categories', methods=['GET'])
def categories():
    categories = Category.get_all(is_json=True)
    return jsonify(categories), 200


@bp.route('/categories/<int:cate_id>', methods=['POST'])
def update_category(cate_id=0):
    if not cate_id:
        raise InvalidUsage('category_id is required')
    cate = Category.get_one_by_id(cate_id)
    if not cate:
        raise InvalidUsage('category_id is invalid')

    sublabel = request.form.get('sublabel', type=str, default='')
    if not sublabel:
        raise InvalidUsage('sublabel is required')

    values ={'sublabel':sublabel}
    category = Category.save(values, cate_id)

    return jsonify(category.to_dict()), 200


@bp.route('/accounts', methods=['GET'])
def accounts():
    items = Account.query.all()
    body = [item.to_dict() for item in items]

    return jsonify(body), 200


@bp.route('/budgets', methods=['GET'])
def budgets():
    items = Budget.get_all()
    #body = [item.to_dict() for item in items]
    return jsonify(items), 200


@bp.route('/budgets/<int:cate_id>', methods=['POST'])
def update_budget(cate_id=0):
    if not cate_id:
        raise InvalidUsage('category_id is required')
    cate = Category.get_one_by_id(cate_id)
    if not cate:
        raise InvalidUsage('category_id is invalid')

    amount = request.form.get('amount', type=int, default=None)
    if amount is None:
        raise InvalidUsage('amount is required')
    amount = int(amount)

    budget = Budget.create(cate_id=cate_id, amount=amount)

    return jsonify(budget.to_dict()), 200


@bp.route('/performance', methods=['GET'])
def performance():
    year, month = validate_month(request.args.get('month'))
    sums = Performance.get_sums_all(year, month)

    return json.dumps(sums), 200


def validate_month(month_str):
    if not month_str:
        raise InvalidUsage('Parameter month is required')
    m = re.search(r'([0-9]{4})\-([0-9]{2})', month_str)
    if not m:
        raise InvalidArgumentException
    year = int(m.group(1))
    month = int(m.group(2))
    if month < 1 or month > 12:
        raise InvalidArgumentException

    return year, month


def validate_presets(form, is_new = False):
    values = {}

    name = form.get('name', type=str, default=None)
    if name is None or not len(name):
        if is_new:
            raise InvalidUsage('name is required')
    else:
        if len(name) > 512:
            raise InvalidUsage('name is too long')
        values['name'] = name

    transaction_name = form.get('transaction_name', type=str)
    values['transaction_name'] = transaction_name

    amount = form.get('amount', type=int, default=None)
    if amount is not None:
        values['amount'] = int(amount)

    account_code = form.get('account_code', type=str, default=None)
    if account_code:
        account = Account.get_one_by_pk(account_code, 'code')
        if not account:
            raise InvalidUsage('account_code is invalid')
        values['account_code'] = account_code

    category_id = int(form.get('category_id', type=int, default=0))
    if category_id:
        category = Category.get_one_by_id(category_id)
        if not category:
            raise InvalidUsage('category is invalid')
        values['category_id'] = category_id

    return values
