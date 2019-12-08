import re
import json
from pprint import pprint
from urllib.parse import unquote_plus
from flask import current_app, jsonify, request
from flask_cors import cross_origin
from . import bp
from app.forms import Contact as ContactForm
from app.models import Contact
from app.email import send_contact_email
from app.common.date import conv_dt_from_utc
from app.common.file import put_to_file
from app.repo_handler import RepoHandler


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


@bp.route('/repos', methods=['POST'])
def repos():
    #if request.headers['Content-Type'] != 'application/json':
    #    print(request.headers['Content-Type'])
    #    return flask.jsonify(res='error'), 400
    payload = request.get_data().decode('utf-8')
    payload = unquote_plus(payload)
    payload = re.sub('payload=', '', payload)
    payload = json.loads(payload)
    # For debug
    payload_json = json.dumps(payload)
    put_to_file('var/repos.json', payload_json+'\n', mode='a')

    repos = current_app.config['GIT_REPOS']
    repo_key = None
    repo = None
    for key, val in repos.items():
        if val['repo_url'] == payload['repository']['url']:
            repo_key = key
            repo = val
            break

    br = payload['ref'].replace('refs/heads/', '').strip()
    handler = RepoHandler()

    if 'revisions' in payload:
        handler.update(repo_key, br)
    elif payload['before'] == '0000000000000000000000000000000000000000':
        handler.create(repo_key, br)
    elif payload['after'] == '0000000000000000000000000000000000000000':
        handler.delete(repo_key, br)

    return payload, 200
