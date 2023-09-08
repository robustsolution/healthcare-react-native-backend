from flask import Blueprint, request, jsonify, send_file
from web_util import assert_data_has_keys, admin_authenticated
from db_util import get_connection
from web_errors import WebError
from users.user import User
from datetime import datetime
from patients.patient import Patient
from patients.data_access import all_patient_data, search_patients
from users.data_access import all_user_data, add_user, delete_user_by_id, user_data_by_email
from language_strings.language_string import LanguageString
from admin_api.patient_data_export import most_recent_export
from admin_api.single_patient_data_export import single_patient_export

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


@admin_api.route('/logout', methods=['POST'])
@admin_authenticated
def logout(admin_user: User):
    admin_user.logout()
    return jsonify({'message': 'OK'})

@admin_api.route('/is_authenticated', methods=['GET'])
@admin_authenticated
def is_authenticated(_admin_user):
    return jsonify({'message': 'OK'})


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
    # language = params.get('language', 'en')
    # name_str = LanguageString(id=str(uuid.uuid4()), content_by_language={language: params['name']})
    hashed_password = bcrypt.hashpw(params['password'].encode(), bcrypt.gensalt()).decode()
    user = User(id, params['name'], params['role'], params['email'], hashed_password)
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


# @admin_api.route('/upload', methods=['POST'])
# @admin_authenticated
# def upload_patient_data(_admin_user):
#     if len(request.files) == 0:
#         raise WebError('Files must be present', 400)

#     importer = PatientDataImporter(request.files['file'])
#     importer.run()
#     return jsonify({'message': 'OK'})


@admin_api.route('/export', methods=['POST'])
@admin_authenticated
def export_all_data(_admin_user):
    export_filename = most_recent_export()
    return send_file(export_filename, attachment_filename='hikma_export.xlsx')


@admin_api.route('/all_patients', methods=['GET'])
@admin_authenticated
def get_all_patients(_admin_user):
    all_patients = [Patient.from_db_row(r).to_dict() for r in all_patient_data()]
    return jsonify({'patients': all_patients})


@admin_api.route('/search_patients', methods=['POST'])
@admin_authenticated
def search(_admin_user):
    params = assert_data_has_keys(request, {'given_name', 'surname', 'country', 'hometown'})
    patient = [Patient.from_db_row(r).to_dict() for r in search_patients(params['given_name'], params['surname'], params['country'], params['hometown'])]
    return jsonify({'patient': patient})
        

@admin_api.route('/export_patient', methods=['POST'])
@admin_authenticated
def export_patient_data(_admin_user):
    params = assert_data_has_keys(request, {'patient_id'})
    export_filename = single_patient_export(params['patient_id'])
    return send_file(export_filename, attachment_filename='hikma_patient_export.xlsx')


@admin_api.route('/summary_stats', methods=['GET'])
@admin_authenticated
def get_summary_stats(_admin_user):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                # get the total counts for patients, events, visits, users and forms
                cur.execute("SELECT COUNT(*) FROM patients")
                patient_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM events")
                event_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM users")
                user_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM event_forms WHERE is_deleted=FALSE")
                form_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM visits")
                visit_count = cur.fetchone()[0]

            except Exception as e:
                print("Error while getting summary stats: ", e)
                raise e
    return jsonify({'patient_count': patient_count, 'event_count': event_count, 'user_count': user_count, 'form_count': form_count, 'visit_count': visit_count})


@admin_api.route('/save_event_form', methods=['POST'])
@admin_authenticated
def save_event_form(_admin_user):
    params = assert_data_has_keys(request, {'event_form'})
    event_form = params['event_form']
    print("event_form: ", event_form)
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO event_forms (id, name, description, metadata, language, is_editable, is_snapshot_form, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        event_form['id'], 
                        event_form['name'], 
                        event_form['description'], 
                        event_form['metadata'], 
                        event_form["language"], 
                        event_form["is_editable"], 
                        event_form["is_snapshot_form"], 
                        event_form['createdAt'], 
                        event_form['updatedAt']
                    )
                )
            except Exception as e:
                conn.rollback()
                print("Error while inserting event form: ", e)
                raise e

    return jsonify({'message': 'OK'})


@admin_api.route('/get_event_forms', methods=['GET'])
@admin_authenticated
def get_event_forms(_admin_user):
    event_forms = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT id, name, description, metadata, language, is_editable, is_snapshot_form, created_at, updated_at FROM event_forms WHERE is_deleted=FALSE")
                for frm in cur.fetchall():
                    event_forms.append({
                        "id": frm[0],
                        "name": frm[1],
                        "description": frm[2],
                        "metadata": frm[3],
                        "language": frm[4],
                        "is_editable": frm[5],
                        "is_snapshot_form": frm[6],
                        "createdAt": frm[7],
                        "updatedAt": frm[8]
                    })
            except Exception as e:
                conn.rollback()
                print("Error while getting event forms: ", e)
                raise e

    return jsonify({'event_forms': event_forms})


@admin_api.route("/update_event_form", methods=["POST"])
@admin_authenticated
def update_event_form(admin_user):
    params = assert_data_has_keys(request, {'id', 'updates'})
    event_form_id = params['id']
    event_form_update = params['updates']
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                updates_str = ", ".join([f"{k}='{event_form_update[k]}'" for k in event_form_update.keys()])
                sqlQuery = "UPDATE event_forms SET " + updates_str + ", updated_at=CURRENT_TIMESTAMP, last_modified = CURRENT_TIMESTAMP WHERE id=" + f"'{event_form_id}'"
                print(updates_str)
                print(sqlQuery)
                cur.execute(sqlQuery)
            except Exception as e:
                conn.rollback()
                print("Error updating event form: ", e)
                raise e
    return jsonify({ 'message': 'OK' })


@admin_api.route('/delete_event_form', methods=['DELETE'])
@admin_authenticated
def delete_event_form(_admin_user):
    params = assert_data_has_keys(request, {'id'})
    event_form_id = params['id']
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                dt = datetime.now()
                # cur.execute("DELETE FROM event_forms WHERE id = %s", (event_form_id,))
                # Flag form as deleted
                cur.execute(f"UPDATE event_forms SET is_deleted=TRUE, deleted_at='{dt}' WHERE id='{event_form_id}'")
            except Exception as e:
                conn.rollback()
                print("Error while deleting event form: ", e)
                raise e

    return jsonify({'message': 'OK'})
