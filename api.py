import hues
from flask import Blueprint, jsonify, request

import celery_tasks

api = Blueprint('api', __name__)


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
