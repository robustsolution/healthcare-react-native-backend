from db_util import get_connection
from patients.patient import Patient
from language_strings.data_access import update_language_string
from language_strings.language_string import to_id


def add_patient(patient: Patient):
    update_language_string(patient.given_name)
    update_language_string(patient.surname)
    update_language_string(patient.country)
    update_language_string(patient.hometown)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO patients (id, given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        [patient.id,
                         to_id(patient.given_name),
                         to_id(patient.surname),
                         patient.date_of_birth,
                         patient.sex,
                         to_id(patient.country),
                         to_id(patient.hometown),
                         patient.phone,
                         patient.edited_at
                         ])