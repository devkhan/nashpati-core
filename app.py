from flask import Flask
from api import api
from config import config
from models import DatabaseWrapper, VideoInfo


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = config['CELERY_RESULT_BACKEND']
app.config['DATABASE'] = config['DATABASE_URL']
db_wrapper = DatabaseWrapper().get_db_wrapper
db_wrapper.init_app(app)
# db_wrapper.database.init(app.config['DATABASE'])
# db_wrapper.database.connect()
db_wrapper.database.create_tables([VideoInfo], safe=True)
db_wrapper.database.close()
app.debug = True
app.register_blueprint(api, url_prefix='/api')


def get_app():
    return app

if __name__ == '__main__':
    app.run(debug=True, port=config['PORT'])
