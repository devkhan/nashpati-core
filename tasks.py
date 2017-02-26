from celery import Celery

from config import config
import hues


celery = Celery(config['APP_NAME'], broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)


@celery.task
def get_video_info(url):
    from youtube_dl import YoutubeDL

    ytdl = YoutubeDL()
    ytdl.add_default_info_extractors()
    info = ytdl.extract_info(url)
    hues.info('URL: ', url)
    hues.info('Video info: ', info)
