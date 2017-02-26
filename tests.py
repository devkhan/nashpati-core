import app
import unittest
import hues


class EndpointsTests(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_404_on_root(self):
        assert (self.app.get('/').status_code == 404)

    def test_video_info_endpoint(self):
        resp = self.app.post('/api/video/info', data=dict())
        hues.log(resp)
        assert resp.status_code == 200

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
