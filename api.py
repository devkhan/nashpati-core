from flask import Blueprint, jsonify, request
from playhouse.flask_utils import get_object_or_404
from models import DatabaseWrapper
from utils import return_json
from models import VideoInfo, Video, Provider

import hues
import celery_tasks


api = Blueprint('api', __name__)
db = DatabaseWrapper().get_db_wrapper.database


# NOTE: This is here for historical reasons, I'll remove it in the future.
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
    if 'video_id' not in req:
        if 'video_web_url' not in req:
            return jsonify({
                'status': 'errored',
                'message': 'Either `video_id` or `video_web_url` must be provided.',
            }), 400
        else:
            v_info.webpage_url = req['video_web_url']
    elif 'provider' not in req:
        return jsonify({
                'status': 'errored',
                'message': '`provider` must be given with `video_id`.',
            }), 400
    else:
        v_info.video_id = req['video_id']
        v_info.provider = req['provider']
    if v_info.save():
        return jsonify(v_info), 201
    else:
        return jsonify({
            'status': 'errored',
            'message': 'Couldn\'t save `VideoInfo` object.',
        })
    # TODO: Add VideoInfo object in database, and start a task with that id.
    # celery_tasks.get_video_info.delay(args)


@api.route('/version', methods=['GET'])
@return_json
def version():
    return {'version': __version__}


__version__ = '0.1.0'
