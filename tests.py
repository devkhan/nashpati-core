import json
import unittest

from flask import Flask

import app

from config import config
from models import VideoInfo

FLASK_APP_HOST = 'http://localhost:%s' % config['PORT']
FLASK_APP = Flask(app.__name__)


class ModelTest(unittest.TestCase):
    def test_can_save_video_info(self):
        with FLASK_APP.app_context():
            vi = VideoInfo()
            vi.url = 'https://www.youtube.com/watch?v=UPW8y6woTBI'
            from youtube_dl import YoutubeDL
            ytdl = YoutubeDL()
            ytdl.add_default_info_extractors()
            vi.ytdl_info = json.dumps(ytdl.extract_info(vi.url, download=False))
            vi.save()
            vi.add_formats()
            vi = VideoInfo.get(VideoInfo.id == vi.get_id())
            self.assertEqual(len(vi.videos), 20, 'number of formats not equal')

if __name__ == '__main__':
    unittest.main()
