from db_util import get_connection
from web_errors import WebError


def user_data_by_email(email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, role, email, hashed_password FROM users WHERE email = %s',
                        [email])
            row = cur.fetchone()
            if not row:
                raise WebError("email not found", status_code=404)
            return row
