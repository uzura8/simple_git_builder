from flask_script import Manager
from app import create_app, db
from app.scraper import Scraper

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
    from app.models import setup_fixurtes
    setup_fixurtes()
    print('Imported default data to DB')


@manager.command
def generate_config_js(output_dir):
    '''Generate config json file'''
    from app.common.site.util import config_js
    from app.common.file import put_json_from_dict
    put_json_from_dict(output_dir, config_js())


@manager.command
def scrape():
    #if not arg:
    #    raise Exception('No Argument')

    scraper = Scraper()
    scraper.main()


if __name__ == '__main__':
    manager.run()
