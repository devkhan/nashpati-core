import app
import unittest
import hues
import requests

from config import config

FLASK_APP_HOST = 'http://localhost:%s' % config['PORT']


class EndpointsTests(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_404_on_root(self):
        assert (self.app.get('/').status_code == 404)

    def test_video_info_endpoint(self):
        # resp = self.app.post('/api/video/info',
        #                      data=dict(video_url='https://www.youtube.com/watch?v=jLbFHFsFCVQ'), )
        resp = requests.post(FLASK_APP_HOST + '/api/video/info', json={
            'video_url': 'https://www.youtube.com/watch?v=jLbFHFsFCVQ'
        })
        hues.log(resp)
        assert resp.status_code == 200

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
