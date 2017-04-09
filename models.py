import json
import time

from playhouse.flask_utils import FlaskDB
from peewee import *
from json import JSONEncoder


class DatabaseWrapper(object):
    _db_wrapper = FlaskDB()

    @property
    def get_db_wrapper(self):
        return DatabaseWrapper._db_wrapper

db_wrapper = DatabaseWrapper().get_db_wrapper


class VideoInfoStatus:
    PENDING = 1
    RUNNING = 2
    SUCCEEDED = 3
    FAILED = 4
    ERRORED = 5
    CHOICES = [
        (PENDING, 'pending'),
        (RUNNING, 'running'),
        (SUCCEEDED, 'succeeded'),
        (FAILED, 'failed'),
        (ERRORED, 'errored'),
    ]


class VideoStatus:
    NOT_DOWNLOADED = -1
    DOWNLOADED = -2
    PARTLY_DOWNLOADED = -3
    DOWNLOADING = -4
    FAILED = -5
    CHOICES = [
        (NOT_DOWNLOADED, 'not downloaded'),
        (DOWNLOADED, 'downloaded'),
        (PARTLY_DOWNLOADED, 'partly downloaded'),
        (DOWNLOADING, 'downloading'),
        (FAILED, 'download failed'),
    ]


class VideoInfo(db_wrapper.Model, JSONEncoder):
    timestamp = TimestampField(null=False, default=int(time.time()))
    url = CharField(max_length=255, null=True)
    ytdl_info = TextField(null=True)
    status = IntegerField(choices=VideoInfoStatus.CHOICES, default=VideoInfoStatus.PENDING)

    def serialize(self):
        serialized = {
            'id': self.get_id(),
            'video_url': self.url,
            'status': self.status,
            'timestamp': self.timestamp,
        }
        if self.ytdl_info:
            serialized.update({
                'info': json.loads(self.ytdl_info)
            })
        return serialized

    def add_formats(self):
        info = self.info
        if not info:
            return
        if 'formats' not in info:
            video = Video()
            video.video_url = info['url']
            video.format = info['format']
            video.video = self.get_id()
            video.save()
            return
        for f in info['formats']:
            video = Video()
            video.video = self.get_id()
            video.video_url = f['url']
            video.format = f['format'] if 'format' in f else ''
            video.total_bytes = f['filesize'] if 'filesize' in f else None
            video._extra = json.dumps(f)
            video.save()
        return

    @property
    def info(self):
        return json.loads(self.ytdl_info)

    class Meta:
        pass


class Video(db_wrapper.Model):
    video = ForeignKeyField(VideoInfo, related_name='videos')
    format = CharField(max_length=50)
    video_url = CharField(max_length=255, null=False)
    downloaded_bytes = IntegerField(null=False, default=0)
    total_bytes = IntegerField(null=True)
    status = IntegerField(choices=VideoStatus.CHOICES, default=VideoStatus.NOT_DOWNLOADED)
    location = CharField(max_length=255, null=True)
    _extra = TextField(null=True)

    def serialized(self):
        serialized = {
            'format': self.format,
            'video_url': self.url,
            'downloaded_bytes': self.downloaded_bytes,
            'total_bytes': self.total_bytes,
            'status': self.status,
            'location': self.location,
            'timestamp': self.timestamp,
        }
        if self.extra:
            serialized.update({
                'extra': self.extra
            })
        return serialized

    @property
    def extra(self):
        return json.loads(self.extra)

    class Meta:
        pass
