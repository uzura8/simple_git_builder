from flask_script import Manager
from app import create_app, db
from app.email import send_email
from app.repo_handler import RepoHandler

app = create_app()
manager = Manager(app)


@manager.command
def setup_db():
    ''' Setup db '''
    db_create()
    db_fixture()
    print('db setup.')


@manager.command
def db_create():
    ''' Setup db '''
    db.create_all()
    print('db created.')


@manager.command
def db_fixture():
    '''Import default data to DB'''
    pass
    #from app.models.brand import setup_fixurtes as setup_fixture_brand
    #setup_fixture_brand()
    #print('Imported default data to DB')


@manager.command
def generate_config_js(output_dir):
    '''Generate config json file'''
    from app.common.site.util import config_js
    from app.common.file import put_json_from_dict
    put_json_from_dict(output_dir, config_js())


@manager.command
@manager.option('-h', '--html', default=0, help='use html format')
def sendmail(email_to, subject, body, html=0):
    '''args: to_email, subject, body'''
    send_email(subject, app.config['FBD_ADMIN_MAIL'], [email_to], text_body=body)


@manager.command
@manager.option('-f', '--force', default=0, help='Set if you want to reset')
@manager.option('-d', '--debug', default=0, help='Set if show details')
def deploy_repo(repo_key, force=0, debug=0):
    '''clone branches in one repo'''
    handler = RepoHandler()
    handler.main(repo_key, force, debug)
    del handler


if __name__ == '__main__':
    manager.run()
