from db_util import get_connection
from web_errors import WebError
import bcrypt
from language_strings.data_access import update_language_string
from datetime import datetime


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


def add_user(user):
    update_language_string(user.name)
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = '''
            INSERT INTO users (id, name, role, email, hashed_password, edited_at) VALUES (%s, %s, %s, %s, %s, %s);
            '''
            cur.execute(query, [user.id, user.name.id, user.role, user.email, user.hashed_password, datetime.now()])
