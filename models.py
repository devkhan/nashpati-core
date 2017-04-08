import json
import time
import hues

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


class VideoInfo(db_wrapper.Model, JSONEncoder):
    timestamp = TimestampField(null=False, default=int(time.time()))
    url = CharField(max_length=255, null=True)
    ytdl_info = TextField(null=True)
    status = IntegerField(choices=VideoInfoStatus.CHOICES, default=VideoInfoStatus.PENDING)

    def serialize(self):
        hues.info('VideoInfo.serialize()')
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

    @property
    def info(self):
        return json.loads(self.ytdl_info)

    class Meta:
        pass


class Video(db_wrapper.Model):
    video_url = CharField(max_length=255)
    location = CharField(max_length=255)
    status = CharField(null=False, default='not-downloaded')
    size = IntegerField(null=True)
    timestamp = TimestampField()
    format = CharField(max_length=50)

    class Meta:
        pass
