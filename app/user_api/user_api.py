from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from users.user import User

user_api = Blueprint('users_api', __name__, url_prefix='/api/user')


@user_api.route('/reset_password', methods=['POST'])
def sync():
    params = assert_data_has_keys(request, {'email', 'password', 'new_password'})
    user = User.authenticate(params['email'], params['password'])
    user.reset_password(params['new_password'])
    return jsonify({'message': 'OK'})
