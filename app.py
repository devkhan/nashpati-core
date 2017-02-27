from flask import Flask
from api import api
from config import config


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = config['CELERY_RESULT_BACKEND']
app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=config['PORT'])
