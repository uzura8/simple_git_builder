from flask import jsonify, request
from . import bp, InvalidUsage
from app.models import Example
from app.common.date import validate_date


@bp.before_request
def before_request():
    pass


@bp.route('/example', methods=['GET', 'POST'])
def example():
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

        example = Example.create(values)
        if example is None:
            raise InvalidUsage('Database save error')

        body = example.to_dict()

    else:
        pass
        #body = [item.to_dict() for item in items]

    return jsonify(body), 200
