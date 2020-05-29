from db_util import get_connection
from language_strings.data_access import update_language_string
from language_strings.language_string import to_id
from datetime import datetime


def add_clinic(clinic):
    update_language_string(clinic.name)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO clinics (id, name, edited_at) VALUES (%s, %s, %s)',
                        [clinic.id, to_id(clinic.name), clinic.edited_at])


def get_most_common_clinic():
    primary = """
    select clinic_id, count(*) from visits where clinic_id is not null group by clinic_id order by count desc limit 1;
    """
    secondary = "SELECT id from clinics;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(primary)
            result = cur.fetchone()
            if not result:
                cur.execute(secondary)
                result = cur.fetchone()
            return result[0]