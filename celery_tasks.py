from celery import Celery
from youtube_dl import YoutubeDL

from config import config
from logger import logger


celery = Celery(config['APP_NAME'], broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)


@celery.task(bind=True)
def get_video_info(self, id):
    ytdl = YoutubeDL()
    ytdl.add_default_info_extractors()
    # TODO: The id param will be used to get the url from the database, and
    # TODO: the task will then be started
    # info = ytdl.extract_info(url, download=False)
    # logger.info('URL: ', url)
    # logger.info('Video info: ', info)
