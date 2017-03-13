from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
from playhouse.flask_utils import get_object_or_404
from models import DatabaseWrapper

import hues
import celery_tasks
import models


api = Blueprint('api', __name__)
rest_api = Api(api)
db = DatabaseWrapper().get_db_wrapper.database


# NOTE: This is here for legacy reasons, I'll remove it in the future.
@api.route('/video/info', methods=['POST'])
def get_video_info():
    body = request.json
    hues.log(body)
    # A pointless end-point for testing purposes.
    celery_tasks.get_video_info.delay(body['video_url'])
    return jsonify({
        'status': 'running',
        'message': 'video submitted successfully'
    })


class VideoRequest(Resource):

    def get(self, id: int):
        with db.atomic():
            video_requests = models.VideoInfo.select().where()
            return get_object_or_404(video_requests, (models.VideoInfo.id == id))

    def put(self):
        video_request = models.VideoInfo()
        video_request.save()



rest_api.add_resource(VideoRequest, '/video')
