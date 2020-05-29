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


def patient_from_key_data(given_name: str, surname: str, country: str, sex: str):
    query = """
    SELECT id FROM patients 
    WHERE get_string(given_name, 'en') = %s AND get_string(surname, 'en') = %s AND get_string(country, 'en') = %s AND sex = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [given_name, surname, country, sex])
            row = cur.fetchone()
            if row is None:
                return None
            return row[0]
