from db_util import get_connection
from language_strings.data_access import update_language_string
from datetime import datetime


def add_clinic(clinic):
    update_language_string(clinic.name)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO clinics (id, name, edited_at) VALUES (%s, %s, %s)',
                        [clinic.id, clinic.name.id, clinic.edited_at])
