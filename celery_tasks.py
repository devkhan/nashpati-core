import json

import hues
from celery import Celery
from flask import Flask
from youtube_dl import YoutubeDL, DownloadError
from youtube_dl.utils import ExtractorError

import app
from config import config
from models import VideoInfo, VideoInfoStatus, Video, VideoStatus


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
            vi_obj.add_formats()
    except (DownloadError, ExtractorError) as e:
        vi_obj.status = VideoInfoStatus.FAILED
    finally:
        vi_obj.save()
    return


@celery.task(bind=True)
def download_video(self, id, format_id):
    f = Video.select().where((Video.video_id == int(id)) & (Video.format_id == format_id)).first()

    def database_update_hook(s):
        hues.info(s)
        if s['status'] == 'error':
            f.status = VideoStatus.FAILED
            f.save()
        if s['status'] == 'finished':
            f.downloaded_bytes = f.total_bytes = s['total_bytes']
            f.status = VideoStatus.DOWNLOADED
            f.save()
    ytdl = YoutubeDL(params={
        'outtmpl': generate_filename(f),
        'progress_hooks': [ database_update_hook ]
    })
    ytdl.add_default_info_extractors()
    f.status = VideoStatus.DOWNLOADING
    f.location = generate_filename(f)
    f.save()
    try:
        ytdl.download(url_list=[f.video_url])
    except:
        f.status = VideoStatus.FAILED
        f.save()
    return


def generate_filename(f):
    return config['DOWNLOAD_PATH'] + '%s_%s.%s' % (str(f.id), str(f.format_id), f.extra['ext'])
