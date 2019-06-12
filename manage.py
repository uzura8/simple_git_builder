from flask_script import Manager
from app import create_app, db
from app.importer import Importer

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
    from app.models.brand import setup_fixurtes as setup_fixture_brand
    setup_fixture_brand()
    print('Imported default data to DB')


@manager.command
def generate_config_js(output_dir):
    '''Generate config json file'''
    from app.common.site.util import config_js
    from app.common.file import put_json_from_dict
    put_json_from_dict(output_dir, config_js())


@manager.command
@manager.option('-m', '--mode', default='all', help='mode:all')
def import_data(brand, mode=''):
    '''option --mode:month, all_month, all'''
    importer = Importer()
    importer.main(brand, mode=mode)
    del importer


if __name__ == '__main__':
    manager.run()
