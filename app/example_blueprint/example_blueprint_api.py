from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
import example_blueprint.data_access as db

example_blueprint_api = Blueprint('example', __name__, url_prefix='/example')


@example_blueprint_api.route('/get_one', methods=['POST'])
def get_one():
    params = assert_data_has_keys(request, {'example_param'})
    _example_param = params['example_param']
    db_result = db.get_one()

    return jsonify({'result': db_result})
