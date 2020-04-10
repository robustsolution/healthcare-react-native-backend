from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from web_errors import WebError
from users.user import User
from sync.db_sychronization import DbSynchronizer


mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api')


@mobile_api.route('/login', methods=['POST'])
def login():
    params = assert_data_has_keys(request, {'email', 'password'})
    user = User.authenticate(params['email'], params['password'])
    return jsonify(user.to_dict())


@mobile_api.route('/sync', methods=['POST'])
def sync():
    params = assert_data_has_keys(request, {'email', 'password'}, data_type='form')
    User.authenticate(params['email'], params['password'])
    if 'db' not in request.files:
        raise WebError('db must be provided', 400)

    synchronizer = DbSynchronizer(request.files['db'])
    if not synchronizer.prepare_sync():
        raise WebError("Synchronization failed", 500)

    synchronizer.execute_server_side_sql()
    return jsonify({'to_execute': synchronizer.get_client_sql()})
