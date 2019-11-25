import os
ENV = os.environ.get('APP_ENV', 'dev_local')


FLASK_DEBUG_PORT = 5000


if ENV in ('dev_local', 'dev_docker'):
    if ENV == 'dev_local':
        PG_HOST = 'localhost'
    elif ENV == 'dev_docker':
        PG_HOST = 'db'

    PG_USER = 'cairn_dev'
    PG_PASSWORD = 'password'
    PG_DB = 'cairn_dev'
    FLASK_DEBUG = True


if ENV == 'prod':
    FLASK_DEBUG = False
    PG_USER = 'cairn_prod'
    PG_PASSWORD = os.environ['DB_PASSWORD']
    PG_HOST = 'localhost'
    PG_DB = 'cairn_prod'
