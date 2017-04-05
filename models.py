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


class Provider(db_wrapper.Model, JSONEncoder):
    name = CharField(primary_key=True, null=False, max_length=64)
    host = CharField(null=False, max_length=255)

    def default(self, o):
        return {
            'id': o.id,
            'name': o.name,
            'host': o.host,
        }

    class Meta:
        pass


class VideoInfo(db_wrapper.Model, JSONEncoder):
    video_id = CharField(max_length=100, null=True)
    provider = ForeignKeyField(rel_model=Provider, null=True)
    title = TextField(null=True)
    timestamp = TimestampField(null=False, default=int(time.time()))
    webpage_url = CharField(max_length=255, null=True)
    ytdl_info = TextField(null=True)
    status = IntegerField(choices=VideoInfoStatus.CHOICES, default=VideoInfoStatus.PENDING)

    def serialize(self):
        hues.info('VideoInfo.serialize()')
        return {
            'status': self.status,
            'timestamp': self.timestamp,
            'id': self.id,
        }

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
