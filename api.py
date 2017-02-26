import hues
from flask import Blueprint, jsonify, request

import tasks

api = Blueprint('api', __name__)


@api.route('/video/info', methods=['POST'])
def get_video_info():
    body = request.json
    hues.log(request)
    # A pointless end-point for testing purposes.
    return jsonify({
        'status': 'running',
        'message': 'video submitted successfully'
    })
