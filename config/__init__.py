class BaseConfig(object):
    FLASKBIRD_VERSION = '0.1.0Alpha'
    FLASKBIRD_ENV = 'local'

    # instance
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None

    # Flask
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    ## Babel
    #LANGUAGES = ['en', 'ja']
    DEFAULT_TIMEZONE = 'UTC'

    # Flaskbird
    FBD_SITE_NAME = 'Sample Site'
    FBD_ADMIN_MAIL = 'admin@example.com'
    FBD_ADMIN_COMPANY_NAME = 'Sample Site Administrator'
    FBD_ADMIN_COMPANY_SITE_URL = 'https://www.example.com/'
    IS_DEBUG_LOGGING = False
    #IS_SEND_ERROR_REPORT_MAIL = False
    ## Modules
    #FBD_MODULES = ['error', 'site', 'media', 'member', 'api']
    #FBD_OPTIONAL_MODULES = []

    # Mail
    MAIL_AWS_SES_ENABLED = False
    MAIL_AWS_SES_REGION = ''
    MAIL_AWS_SES_ACCESS_KEY_ID = ''
    MAIL_AWS_SES_SECRET_ACCESS_KEY = ''
    MAIL_SERVER = None
    MAIL_PORT = 25
    MAIL_USE_TLS = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    #ADMINS = None
    IS_LOGGING_MAIL = False

    ## Request params
    #PARAMS_LIST_DEFAULT = {
    #    'per_page': 10,
    #    'per_page_max': 100,
    #}

    ## Upload
    #MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    #MEDIA_DIR_NAME = 'media'
    #NOIMAGE_FILE_NAME = 'noimage.png'
    #UPLOAD_SPLIT_DIRS_COUNT = 10
    #UPLOAD_ALLOWED_MEDIA = {
    #    'photo':{
    #        'types':{
    #            'jpeg':'image/jpeg',
    #            'jpg':'image/jpeg',
    #            'png':'image/png',
    #            'gif':'image/gif',
    #        },
    #        'sizes':['200x200xc', '600x600'],
    #    }
    #}

    CORS_RESOURCES = {}

    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY= ''
    RECAPTCHA_PRIVATE_KEY=''
    RECAPTCHA_OPTIONS = {}

    ## contact form
    CONTACT_USE_RECAPTCHA = False
    CONTACT_EMAIL_IS_CHECK_DNS = True
    CONTACT_EMAIL_FROM_NAME = FBD_ADMIN_COMPANY_NAME
    CONTACT_SUBJECT = 'お問い合わせを受け付けました'
    CONTACT_TYPE_CHOICES = [
        ('1', 'サイトについて'),
        ('2', '不具合について'),
        ('3', 'その他')
    ]

    BUILD_CMDS = {}
    BUILD_USER = ''
    GIT_COMMON = {
        'domain': 'example.com',
        'work_dir': '/var/www/work',
        'path': '/var/www/sites',
    }
    GIT_REPOS = {}

