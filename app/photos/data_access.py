from db_util import get_connection


def all_photo_filenames():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT patient_id, filename FROM photos')
            yield from cur


def set_patient_filename(patient_id, base_filename):
    query = '''
    INSERT INTO photos (patient_id, filename) VALUES (%s, %s)
    ON CONFLICT (patient_id) DO UPDATE SET filename=EXCLUDED.filename
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id, base_filename])


def photo_filename_by_patient(patient_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT filename FROM photos WHERE patient_id = %s', [patient_id])
            result = cur.fetchone()
            return result[0] if result else None