from flask import Flask
from api import api
from config import config
from playhouse.flask_utils import FlaskDB


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = config['CELERY_RESULT_BACKEND']
app.register_blueprint(api, url_prefix='/api')
app.config['DATABASE'] = config['DATABASE_URL']
db_wrapper = FlaskDB(app, 'sqlite:///nashpati.db')
app.debug = True


if __name__ == '__main__':
    app.run(debug=True, port=config['PORT'])
