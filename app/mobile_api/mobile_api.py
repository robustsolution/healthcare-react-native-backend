from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from users.user import User

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/api')


@mobile_api.route('/login', methods=['POST'])
def login():
    params = assert_data_has_keys(request, {'email', 'password'})
    user = User.authenticate(params['email'], params['password'])
    return jsonify(user.to_dict())
