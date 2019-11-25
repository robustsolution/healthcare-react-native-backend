from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api')


@mobile_api.route('/get_one', methods=['POST'])
def get_one():
    params = assert_data_has_keys(request, {'example_param'})
    _example_param = params['example_param']

    return jsonify({'result': 'ok'})
