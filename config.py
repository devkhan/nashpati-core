import os
import hues


config = {
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0',
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'DATABASE_URL': 'sqlite:///' + os.getcwd() + '/nashpati.db',
    'DOWNLOAD_PATH': '/temp/',
    'APP_NAME': 'nashpati',
    'PORT': 4444
}
