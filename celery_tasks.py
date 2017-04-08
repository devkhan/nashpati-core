import json

import hues
from celery import Celery
from flask import Flask
from peewee import SqliteDatabase
from youtube_dl import YoutubeDL, DownloadError
from youtube_dl.utils import ExtractorError

from config import config
from models import VideoInfo, VideoInfoStatus
import app


def make_celery():
    celery = Celery(config['APP_NAME'], broker=config['CELERY_BROKER_URL'])
    celery.conf.update(config)
    TaskBase = celery.Task
    fapp = Flask(app.__name__)

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with fapp.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()


@celery.task(bind=True)
def get_video_info(self, id):
    vi_obj = VideoInfo.get(VideoInfo.id == id)
    ytdl = YoutubeDL()
    ytdl.add_default_info_extractors()
    vi_obj.status = VideoInfoStatus.RUNNING
    vi_obj.save()
    try:
        info = ytdl.extract_info(vi_obj.url, download=False)
        if info:
            vi_obj.ytdl_info = json.dumps(info)
            vi_obj.status = VideoInfoStatus.SUCCEEDED
    except (DownloadError, ExtractorError) as e:
        vi_obj.status = VideoInfoStatus.FAILED
    finally:
        vi_obj.save()

