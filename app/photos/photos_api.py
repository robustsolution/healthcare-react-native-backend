from flask import Blueprint, request, jsonify, send_file
from web_util import assert_data_has_keys
from web_errors import WebError
from photos.data_access import all_photo_filenames, photo_filename_by_patient, set_patient_filename
from photos.photo_storage import store_photo, retrieve_photo
from users.user import User


photos_api = Blueprint('photos_api', __name__, url_prefix='/api/photos')


@photos_api.route('/metadata', methods=['POST'])
def metadata():
    params = assert_data_has_keys(request, {'email', 'password'})
    User.authenticate(params['email'], params['password'])
    return jsonify(dict(all_photo_filenames()))


@photos_api.route('/get_photo', methods=['POST'])
def get_photo():
    params = assert_data_has_keys(request, {'email', 'password', 'patient_id'})
    User.authenticate(params['email'], params['password'])
    base_filename = photo_filename_by_patient(params['patient_id'])
    if base_filename is None:
        raise WebError('Patient photo unavailable', 404)
    filename = retrieve_photo(base_filename)
    if filename is None:
        raise WebError('Patient photo unavailable', 404)
    return send_file(filename)


@photos_api.route('/set_photo', methods=['POST'])
def set_photo():
    params = assert_data_has_keys(request, {'email', 'password', 'patient_id'}, data_type='form')
    User.authenticate(params['email'], params['password'])
    if 'photo' not in request.files:
        raise WebError('photo must be provided', 400)
    base_filename = store_photo(request.files['photo'])
    set_patient_filename(params['patient_id'], base_filename)
    return jsonify({'message': 'ok'})