from playhouse.flask_utils import FlaskDB
from peewee import *


class DatabaseWrapper(object):
    _db_wrapper = FlaskDB()

    @property
    def get_db_wrapper(self):
        return DatabaseWrapper._db_wrapper

db_wrapper = DatabaseWrapper().get_db_wrapper


class Provider(db_wrapper.Model):
    name = CharField(primary_key=True, null=False, max_length=64)
    host = CharField(null=False, max_length=255)

    class Meta:
        pass


class VideoRequest(db_wrapper.Model):
    video_id = CharField(max_length=100)
    provider = ForeignKeyField(rel_model=Provider)
    title = TextField(null=True)
    timestamp = TimestampField(null=False)
    webpage_url = CharField(max_length=255, null=True)
    ytdl_info = TextField(null=True)

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
