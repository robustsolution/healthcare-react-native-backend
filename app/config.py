import os
ENV = os.environ.get('APP_ENV', 'dev_local')

FLASK_DEBUG_PORT = 5000

if ENV in ('dev_local', 'dev_docker', 'stg'):
    if ENV in ('dev_local', 'stg'):
        PG_HOST = 'localhost'
    elif ENV == 'dev_docker':
        PG_HOST = 'db'

    PG_USER = 'hikma_dev'
    PG_PASSWORD = 'password'
    PG_DB = 'hikma_dev'
    FLASK_DEBUG = True
    PHOTOS_STORAGE_BUCKET = 'dev-api-photos'
    LOCAL_PHOTO_STORAGE_DIR = '/tmp/hikma_photos'

if ENV == 'prod':
    FLASK_DEBUG = False
    PG_USER = os.environ['DB_NAME']
    PG_PASSWORD = os.environ['DB_PASSWORD']
    PG_HOST = 'localhost'
    PG_DB = os.environ['DB_NAME']
    PHOTOS_STORAGE_BUCKET = os.environ['PHOTOS_STORAGE_BUCKET']
    LOCAL_PHOTO_STORAGE_DIR = '/tmp/hikma_photos'
