from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys, admin_authenticated
from users.user import User
from users.data_access import all_user_data


admin_api = Blueprint('admin_api', __name__, url_prefix='/admin_api')


@admin_api.route('/login', methods=['POST'])
def login():
    params = assert_data_has_keys(request, {'email', 'password'})
    user = User.authenticate(params['email'], params['password'])
    token = user.create_token()
    return jsonify({'token': token})


@admin_api.route('/all_users', methods=['GET'])
@admin_authenticated
def get_all_users(_admin_user):
    all_users = [User.from_db_row(r).to_dict() for r in all_user_data()]
    return jsonify({'users': all_users})
