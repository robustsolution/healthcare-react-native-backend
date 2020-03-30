from db_util import get_connection
from web_errors import WebError
import bcrypt


def user_data_by_email(email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, role, email, hashed_password FROM users WHERE email = %s',
                        [email])
            row = cur.fetchone()
            if not row:
                raise WebError("email not found", status_code=404)
            return row

def update_password(user_id, new_password):
    with get_connection() as conn:
        with conn.cursor() as cur:
            new_password_hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cur.execute('UPDATE users SET hashed_password = %s WHERE id = %s',
                        [new_password_hashed, user_id])