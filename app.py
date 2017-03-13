from flask import Flask
from api import api
from config import config
from models import DatabaseWrapper


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = config['CELERY_RESULT_BACKEND']
app.config['DATABASE'] = 'sqlite:///nashpati.db'
db_wrapper = DatabaseWrapper().get_db_wrapper
db_wrapper.init_app(app)
app.debug = True
app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, port=config['PORT'])
