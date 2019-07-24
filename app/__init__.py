import os
import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.dirname(os.path.abspath(__file__)) + '/../instance',
        static_folder='statics',
        template_folder='templates')

    jinja_options = app.jinja_options.copy()
    jinja_options.update({
        'block_start_string': '[%',
        'block_end_string': '%]',
        'variable_start_string': '[[',
        'variable_end_string': ']]',
        'comment_start_string': '[#',
        'comment_end_string': '#]'
    })
    app.jinja_options = jinja_options

    from instance.config import FLASKBIRD_ENV
    env = FLASKBIRD_ENV
    
    print(app.instance_path)
    app.config.from_object('config.{}.{}Config'.format(env, env.capitalize()))
    app.config.from_pyfile('config.py') #from instance dir
    app.config['ENV'] = env

    db.init_app(app)
    mail.init_app(app)
    cors = CORS(app,
            resources=app.config['CORS_RESOURCES'],
            support_credentials=True)

    modules = ('site', 'api')
    for module_name in modules:
        m = importlib.import_module('app.' + module_name)
        app.register_blueprint(m.bp)

    return app

import app.models

class InvalidArgumentException(HTTPException):
    code = 400
    description = 'Invalid Argument'


class InvalidParameterException(HTTPException):
    code = 400
    description = 'Invalid Parameter'


class InvalidMediaPathException(HTTPException):
    code = 400
    description = 'Invalid media File path'


class NotAcceptableException(HTTPException):
    code = 406
    description = 'Not Acceptable'
