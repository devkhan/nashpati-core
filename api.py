from flask import Blueprint, jsonify, request, current_app
from playhouse.flask_utils import get_object_or_404

from models import DatabaseWrapper
from utils import return_json
from models import VideoInfo

import hues
import celery_tasks


api = Blueprint('api', __name__)
db = DatabaseWrapper().get_db_wrapper.database


@api.before_request
def ensures_content_type():
    if request.method != 'GET' and request.content_type != 'application/json':
        return jsonify({
            'message': 'Content-Type must be application/json'
        }), 415


@api.route('/video/', methods=['POST'])
def submit_new_video_info():
    req = request.json
    hues.info(req)
    v_info = VideoInfo()
    if 'url' not in req:
        return jsonify({
            'status': 'errored',
            'message': '`url` must be provided.',
        }), 400
    else:
        v_info.url = req['url']
    if v_info.save():
        celery_tasks.get_video_info.delay(id=v_info.get_id())
        return jsonify(v_info.serialize()), 201
    else:
        return jsonify({
            'status': 'errored',
            'message': 'Couldn\'t process video URL.',
        }), 500


@api.route('/video/<id>', methods=['GET'])
def get_video_info(id):
    vi = get_object_or_404(VideoInfo.select(), (VideoInfo.id == id))
    if vi:
        return jsonify(vi.serialize()), 200
    return 404


@api.route('/version', methods=['GET'])
@return_json
def version():
    return {'version': __version__}


__version__ = '0.1.0'
