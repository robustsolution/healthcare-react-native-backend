from db_util import get_connection
from patients.patient import Patient
from language_strings.data_access import update_language_string
from language_strings.language_string import to_id, LanguageString


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
    where_clauses = []
    params = []
    if given_name is not None:
        where_clauses.append("get_string(given_name, 'en') = %s")
        params.append(given_name)
    else:
        where_clauses.append("get_string(given_name, 'en') is null")

    if surname is not None:
        where_clauses.append("get_string(surname, 'en') = %s")
        params.append(surname)
    else:
        where_clauses.append("get_string(surname, 'en') is null")

    if country is not None:
        where_clauses.append("get_string(country, 'en') = %s")
        params.append(country)
    else:
        where_clauses.append("get_string(country, 'en') is null")

    if sex is not None:
        where_clauses.append("sex = %s")
        params.append(sex)
    else:
        where_clauses.append('sex is null')

    where_clause = ' AND '.join(where_clauses)

    query = f"SELECT id FROM patients WHERE {where_clause};"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            if row is None:
                return None
            return row[0]

def all_patient_data():
    query = """
    SELECT id, given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at FROM patients ORDER BY edited_at DESC LIMIT 25
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])
            yield from cur

def search_patients(given_name: str, surname: str, country: str, hometown: str):
    where_clauses = []
    params = []
    if given_name is not None:
        where_clauses.append("UPPER(get_string(given_name, 'en')) LIKE %s")
        params.append(f'%{given_name.upper()}%')

    if surname is not None:
        where_clauses.append("UPPER(get_string(surname, 'en')) LIKE %s")
        params.append(f'%{surname.upper()}%')

    if country is not None:
        where_clauses.append("UPPER(get_string(country, 'en')) LIKE %s")
        params.append(f'%{country.upper()}%')

    if hometown is not None:
        where_clauses.append("UPPER(get_string(hometown, 'en')) LIKE %s")
        params.append(f'%{hometown.upper()}%')

    where_clause = ' AND '.join(where_clauses)

    query = f"SELECT id, given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at FROM patients WHERE {where_clause};"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            yield from cur

def patient_from_id(patient_id):
    query = """
    SELECT given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at FROM patients WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id])
            row = cur.fetchone()
            if row is None:
                return None
            given_name, surname, date_of_birth, sex, country, hometown, phone, edited_at = row
            return Patient(
                id=patient_id,
                given_name=LanguageString.from_id(given_name),
                surname=LanguageString.from_id(surname),
                date_of_birth=date_of_birth,
                sex=sex,
                country=LanguageString.from_id(country),
                hometown=LanguageString.from_id(hometown),
                phone=phone,
                edited_at=edited_at
            )

