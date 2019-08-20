from flask import current_app, jsonify, request
from flask_cors import cross_origin
from . import bp
from app.forms import Contact as ContactForm
from app.models import Contact
from app.email import send_contact_email
from app.common.date import conv_dt_from_utc


@bp.before_request
def before_request():
    pass


@bp.route('/contact', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def contact():
    if request.method == 'POST':
        form = ContactForm()
        form.contact_type.choices = current_app.config['CONTACT_TYPE_CHOICES']
        if form.validate_on_submit():
            vals = form.get_dict()
            vals['subject'] = current_app.config['CONTACT_SUBJECT']
            vals['ip'] = request.remote_addr
            vals['ua'] = request.headers.get('User-Agent')
            contact = Contact.create(vals)
            body = contact.to_dict()

            types = form.contact_type.choices
            body['contact_type_label'] = [ label for val, label in types\
                                    if int(val) == body['contact_type'] ][0]

            if not current_app.config['DEFAULT_TIMEZONE']:
                body['created_at_formatted'] = body['created_at'].\
                                                    strftime('%Y/%m/%d %H:%M')
            else:
                body['created_at_formatted'] = conv_dt_from_utc(
                    body['created_at'],
                    current_app.config['DEFAULT_TIMEZONE'],
                    '%Y/%m/%d %H:%M'
                )

            send_contact_email(body['email'], body['subject'], body)

        else:
            body = {'errors':form.errors}
            return jsonify(body), 400
    else:
        body = {'hoge':'fuga'}

    return jsonify(body), 200

