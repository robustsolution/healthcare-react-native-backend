from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys, admin_authenticated
from web_errors import WebError
from users.user import User
from users.data_access import all_user_data, add_user, delete_user_by_id, user_data_by_email
from language_strings.language_string import LanguageString
from admin_api.patient_data_import import PatientDataImporter

import uuid
import bcrypt
import psycopg2.errors


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


@admin_api.route('/user', methods=['POST'])
@admin_authenticated
def create_user(_admin_user):
    params = assert_data_has_keys(request, {'email', 'password', 'name', 'role'})
    if params['role'] not in ['admin', 'provider']:
        raise WebError('Role must be either "admin" or "provider"', 400)

    id = str(uuid.uuid4())
    language = params.get('language', 'en')
    name_str = LanguageString(id=str(uuid.uuid4()), content_by_language={language: params['name']})
    hashed_password = bcrypt.hashpw(params['password'].encode(), bcrypt.gensalt()).decode()
    user = User(id, name_str, params['role'], params['email'], hashed_password)
    try:
        add_user(user)
    except psycopg2.errors.UniqueViolation:
        raise WebError('User already exists', 409)

    all_users = [User.from_db_row(r).to_dict() for r in all_user_data()]
    return jsonify({'users': all_users})


@admin_api.route('/user', methods=['DELETE'])
@admin_authenticated
def delete_user(_admin_user):
    params = assert_data_has_keys(request, {'email'})
    user = User.from_db_row(user_data_by_email(params['email']))
    delete_user_by_id(user.id)
    all_users = [User.from_db_row(r).to_dict() for r in all_user_data()]
    return jsonify({'users': all_users})


@admin_api.route('/change_password', methods=['POST'])
@admin_authenticated
def change_password(_admin_user):
    params = assert_data_has_keys(request, {'email', 'new_password'})
    user = User.from_db_row(user_data_by_email(params['email']))
    user.reset_password(params['new_password'])
    return jsonify({'message': 'ok'})


@admin_api.route('/upload', methods=['POST'])
@admin_authenticated
def upload_patient_data(_admin_user):
    if len(request.files) == 0:
        raise WebError('Files must be present', 400)

    importer = PatientDataImporter(request.files['file'])
    importer.run()
    return jsonify({'message': 'OK'})