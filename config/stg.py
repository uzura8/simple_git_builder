from config import BaseConfig

class StgConfig(BaseConfig):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    CORS_RESOURCES = {r'/api/*': {'origins': ['https://aws-stg.pal-relations.co.jp']}}
